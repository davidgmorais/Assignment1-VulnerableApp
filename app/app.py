import os
from flask import Flask, render_template, request, make_response, url_for, redirect
import database.database_manager as database
import hashlib

FILE_DIR = "./static/data/"
COOKIE_MAX_AGE = 5*60
config = {
    'host': 'localhost',
    'port': 3306,
    'user': os.environ["USER"],
    'password': os.environ["PASSWORD"],
    'database': os.environ["DATABASE"]
}


app = Flask(__name__)
mysql = database.connect(app, config)
if not mysql:
    print("Error connection to database, exiting.")
    exit(1)


@app.route('/', methods=["GET"])
def index():
    loggedIn = True if request.cookies.get("loggedin") == "true" else False
    user = request.cookies.get("user")
    if user and not database.user_exists(mysql, user):
        user = None
        loggedIn = None

    feature_prods = database.get_products(mysql)
    if len(feature_prods) > 4: feature_prods=feature_prods[0:4]
    resp = make_response(render_template('index.html', isloggedIn=loggedIn, feature_prods=feature_prods, user=user))
    if loggedIn and user:
        resp.set_cookie(key='loggedin', value= 'true', max_age=COOKIE_MAX_AGE)
        resp.set_cookie(key='user', value=user, max_age=COOKIE_MAX_AGE)
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():

    loggedIn = True if request.cookies.get("loggedin") == "true" else False
    user = request.cookies.get("user")
    if loggedIn and user and database.user_exists(mysql, user):
        return redirect(url_for('index'))

    if request.method == "POST":

        if request.json:
            _email = request.json.get("email")
            _password = request.json.get("password")
            _password = hashlib.sha256(_password.encode(encoding='utf-8')).hexdigest()

            if database.authenticate_user(mysql, _email, _password):
                resp = make_response("Suceess", 200)
                
                resp.set_cookie(key='loggedin', value= 'true', max_age=COOKIE_MAX_AGE)
                resp.set_cookie(key='user', value=_email, max_age=COOKIE_MAX_AGE)
                return resp

            if database.user_exists(mysql, _email):
                return make_response("Invalid password", 403)
            return make_response("Invalid email", 401)
    
        return render_template('login.html')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":

        if request.json:
            _username = request.json.get("username")
            _email = request.json.get("email")
            _password = request.json.get("password")

            if _username and _email and _password:
                _password = hashlib.sha256(_password.encode(encoding='utf-8')).hexdigest()
                
                if database.register_user(mysql, _username, _email, _password):
                    return make_response("User registered successfully", 201)

            return make_response("Invalid parameters", 400)         

    return render_template('register.html')



@app.route("/addproduct", methods=["GET", "POST"])
def add_product():
    if "loggedin" not in request.cookies or "user" not in request.cookies:
        return make_response("User not authenticated", 401)

    loggedIn = True if request.cookies.get("loggedin") == "true" else False
    email = request.cookies.get("user")
    if not loggedIn:
        return make_response("User not authenticated", 401)
    if not database.user_exists(mysql, email):
        return make_response("User not authenticated", 401)

    if request.method == "POST":
        print(request.form)
        if request.files :
            _filename = request.headers.get("Content-Disposition").split("filename=")[-1]
            _filename= _filename.replace('"', '').replace("'",'')
            _stream = request.files.get("Image")

            with open(FILE_DIR + _filename, "wb") as f:
                f.write(_stream.read())

            user_id = database.get_user_by_email(mysql, email)
            if database.create_product(mysql, request.form, _filename, user_id):
                resp = make_response("Product successfully created", 201)
                resp.set_cookie(key='loggedin', value= 'true', max_age=COOKIE_MAX_AGE)
                resp.set_cookie(key='user', value=email, max_age=COOKIE_MAX_AGE)
                return resp
            resp = make_response("Invalid parameters", 400)
            resp.set_cookie(key='loggedin', value= 'true', max_age=COOKIE_MAX_AGE)
            resp.set_cookie(key='user', value=email, max_age=COOKIE_MAX_AGE)
            return resp     
 

    categories = database.get_categories(mysql)
    conditions = database.get_conditions(mysql)

    resp = make_response(render_template("addProduct.html", categories=categories, conditions=conditions))
    resp.set_cookie(key='loggedin', value= 'true', max_age=COOKIE_MAX_AGE)
    resp.set_cookie(key='user', value=email, max_age=COOKIE_MAX_AGE)
    return resp

@app.route("/product/<product_id>", methods=["GET"])
def get_product(product_id):
    loggedIn = True if request.cookies.get("loggedin") == "true" else False
    user = request.cookies.get("user")
    if user and not database.user_exists(mysql, user):
        user = None
        loggedIn = None

    product = database.get_product_by_id(mysql, product_id)
    resp = make_response(render_template("productDetails.html", product=product))
    if loggedIn and user:
        resp.set_cookie(key='loggedin', value= 'true', max_age=COOKIE_MAX_AGE)
        resp.set_cookie(key='user', value=user, max_age=COOKIE_MAX_AGE)
    
    return resp

@app.route("/product", methods=["GET"])
def products():
    loggedIn = True if request.cookies.get("loggedin") == "true" else False
    user = request.cookies.get("user")
    if user and not database.user_exists(mysql, user):
        user = None
        loggedIn = None

    if 'q' in request.args:
        products = database.search_products(mysql, request.args['q'])
    else:
        products = database.get_products(mysql)
    resp = make_response(render_template("product.html", products=products))
    if loggedIn and user:
        resp.set_cookie(key='loggedin', value= 'true', max_age=COOKIE_MAX_AGE)
        resp.set_cookie(key='user', value=user, max_age=COOKIE_MAX_AGE)
    
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
