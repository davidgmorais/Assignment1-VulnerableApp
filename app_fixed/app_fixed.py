import os
import re
from flask import Flask, render_template, request, make_response, url_for, redirect
import database.database_manager as database
import hashlib
import uuid
from hmac import compare_digest

FILE_DIR = "./static/data/"
COOKIE_MAX_AGE = 5*60
config = {
    'host': 'localhost',
    'port': 3306,
    'user': os.environ["USER"],
    'password': os.environ["PASSWORD"],
    'database': os.environ["DATABASE"],
    'UPLOAD_EXTENSIONS': ['.jpg', '.png', '.jpeg'],
    'secret': os.environ["SECRET"]
}


app = Flask(__name__)
mysql = database.connect(app, config)
if not mysql:
    print("Error connection to database, exiting.")
    exit(1)

def __generate_cookie(email):
    hash = hashlib.sha3_256()
    cookie = f'loggedin=true,user={email}'
    hash.update(bytes(config['secret'],'utf-8'))
    hash.update(bytes(cookie, 'utf-8'))

    return f'{cookie},signature={hash.hexdigest()}'

def __verify_cookie(cookie):
    loggedin, user, signature = cookie.split(',')
    hash = hashlib.sha3_256()
    hash.update(bytes(config['secret'],'utf-8'))
    hash.update(bytes(f'{loggedin},{user}', 'utf-8'))    
    signature_to_verify = f'signature={hash.hexdigest()}'
    
    return compare_digest(signature, signature_to_verify)


@app.route('/', methods=["GET"])
def index():
    loggedIn, user = None, None

    auth = request.cookies.get("auth")
    if auth:
        if __verify_cookie(auth):
            loggedIn, user, _ = auth.split(',')
            loggedIn = loggedIn.split("loggedin=")[1]
            user = user.split("user=")[1]

            if user and not database.user_exists(mysql, user):
                auth = None
                loggedIn, user = None, None
            
        else:
            auth = None

    feature_prods = database.get_products(mysql)
    if len(feature_prods) > 4: feature_prods=feature_prods[0:4]
    resp = make_response(render_template('index.html', isloggedIn=loggedIn, feature_prods=feature_prods, user=user))
    if auth:
        resp.set_cookie(key='auth', value=auth, max_age=COOKIE_MAX_AGE)

    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():

    auth = request.cookies.get("auth")
    if auth and __verify_cookie(auth):
        loggedIn, user, _ = auth.split(',')
        loggedIn = loggedIn.split("loggedin=")[1]
        user = user.split("user=")[1]

        if loggedIn and loggedIn=="true" and user and database.user_exists(mysql, user):
            return redirect(url_for('index'))

    if request.method == "POST":

        if request.json:
            _email = request.json.get("email")
            _password = request.json.get("password")
            _password = hashlib.sha256(_password.encode(encoding='utf-8')).hexdigest()

            if database.authenticate_user(mysql, _email, _password):
                resp = make_response("Suceess", 200)
                _cookie = __generate_cookie(_email)
                resp.set_cookie(key='auth', value=_cookie, max_age=COOKIE_MAX_AGE)
                return resp

            return make_response("Invalid credentials", 401)
    
        return render_template('login.html')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":

        if request.json:
            _username = request.json.get("username")
            _email = request.json.get("email")
            _password = request.json.get("password")

            if not _username or not _email or not _password:
                return make_response("Invalid parameters", 400)  

            if len(_password) < 8:
                return make_response("Invalid parameters", 400)  

            if not any(char.isdigit() for char in _password) or not any(char.isalpha() for char in _password):
                return make_response("Invalid parameters", 400)  

            if not any(char.islower() for char in _password) or not any(char.isupper() for char in _password):
                return make_response("Invalid parameters", 400)  

            if not re.compile('[@_!$%^&*()<>?/\|}{~:]#').search(_password):
                return make_response("Invalid parameters", 400)  

            _password = hashlib.sha256(_password.encode(encoding='utf-8')).hexdigest()
                
            if database.register_user(mysql, _username, _email, _password):
                return make_response("User registered successfully", 201)

        return make_response("Invalid parameters", 400)         

    return render_template('register.html')



@app.route("/addproduct", methods=["GET", "POST"])
def add_product():
    if "auth" not in request.cookies:
        return make_response("User not authenticated", 401)

    auth = request.cookies.get("auth")
    if auth and __verify_cookie(auth):
        loggedIn, user, _ = auth.split(',')
        loggedIn = loggedIn.split("loggedin=")[1]
        user = user.split("user=")[1]

        if (loggedIn and loggedIn!="true") or (user and not database.user_exists(mysql, user)):
            return make_response("User not authenticated", 401)

    if request.method == "POST":

        if request.files :
            invalid_resp = make_response("Invalid parameters", 400)
            invalid_resp.set_cookie(key='auth', value=auth, max_age=COOKIE_MAX_AGE)
            
            _filename = request.headers.get("Content-Disposition").split("filename=")[-1]
            _filename= _filename.replace('"', '').replace("'",'')

            if _filename == '':
                return invalid_resp     

            file_ext = os.path.splitext(_filename)[1]
            if file_ext not in config['UPLOAD_EXTENSIONS']:
                return invalid_resp

            _stream = request.files.get("Image")
            _filename = uuid.uuid4().hex + file_ext

            print(_filename)
            with open(FILE_DIR + _filename, "wb") as f:
                f.write(_stream.read())

            user_id = database.get_user_by_email(mysql, user)
            if database.create_product(mysql, request.form, _filename, user_id):
                resp = make_response("Product successfully created", 201)
                resp.set_cookie(key='auth', value= auth, max_age=COOKIE_MAX_AGE)
                return resp
            
            return invalid_resp     

    categories = database.get_categories(mysql)
    conditions = database.get_conditions(mysql)

    resp = make_response(render_template("addProduct.html", categories=categories, user=user, isloggedIn=loggedIn, conditions=conditions))
    resp.set_cookie(key='auth', value=auth, max_age=COOKIE_MAX_AGE)
    return resp


@app.route("/product/<product_id>", methods=["GET"])
def get_product(product_id):
    loggedIn, user = None, None
    auth = request.cookies.get("auth")
    if auth:
        if  __verify_cookie(auth):
            loggedIn, user, _ = auth.split(',')
            loggedIn = loggedIn.split("loggedin=")[1]
            user = user.split("user=")[1]

            if (loggedIn and loggedIn!="true") or (user and not database.user_exists(mysql, user)):
                auth = None
                loggedIn, user = None, None
        else:
            auth = None

    product = database.get_product_by_id(mysql, product_id)
    resp = make_response(render_template("productDetails.html", product=product, user=user, isloggedIn=loggedIn))
    if auth:
        resp.set_cookie(key='auth', value=auth, max_age=COOKIE_MAX_AGE)
    
    return resp


@app.route("/product", methods=["GET"])
def products():
    loggedIn, user = None, None
    auth = request.cookies.get("auth")
    if auth:
        if  __verify_cookie(auth):
            loggedIn, user, _ = auth.split(',')
            loggedIn = loggedIn.split("loggedin=")[1]
            user = user.split("user=")[1]

            if (loggedIn and loggedIn!="true") or (user and not database.user_exists(mysql, user)):
                auth = None
                loggedIn, user = None, None
        else:
            auth = None

    if 'q' in request.args:
        products = database.search_products(mysql, request.args['q'])
    else:
        products = database.get_products(mysql)
    resp = make_response(render_template("product.html", products=products, user=user, isloggedIn=loggedIn))
    if auth:
        resp.set_cookie(key='auth', value=auth, max_age=COOKIE_MAX_AGE)
    
    return resp


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000)
    app.run(debug=True)