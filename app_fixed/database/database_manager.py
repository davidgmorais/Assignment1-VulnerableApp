from math import prod
from multiprocessing import Condition
from os import curdir
import queue
import time

from graphql_relay import cursor_for_object_in_connection
from models.Product import Product
from flaskext.mysql import MySQL

MAX_TRIES = 5

def connect(app, config):
    app.config['MYSQL_DATABASE_USER'] = config['user']
    app.config['MYSQL_DATABASE_PASSWORD'] = config['password']
    app.config['MYSQL_DATABASE_DB'] = config['database']
    app.config['MYSQL_DATABASE_HOST'] = config['host'] 
    app.config['MYSQL_DATABASE_PORT'] = config['port'] 

    for i in range(MAX_TRIES):
        try:
            mysql = MySQL(app)
            return mysql
        except mysql.connector.Error:
            print("Error connection to database, retrying in 5seconds...")
            time.sleep(3)

    return None

def register_user(mysql, username, email, password):
    if not mysql:
        return None

    try:
        cursor = mysql.get_db().cursor()
        cursor.execute("INSERT INTO USER(name, email, password) VALUES (%s, %s, %s);", (username, email, password))
        mysql.get_db().commit()
        cursor.close()
        return True

    except Exception as err:
        print(err)
    return False

def user_exists(mysql, email):
    if not mysql:
        return None

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id FROM USER WHERE email = %s;", email)
    user = cursor.fetchone()
    cursor.close()

    if user: return True
    return False

def authenticate_user(mysql, email, password):
    if not mysql:
        return None

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT email, password FROM USER WHERE email = %s", email)
    user = cursor.fetchone()
    cursor.close()

    if user and password == user[1]:
        return True

    return False

def get_user_by_email(mysql, email):
    if not mysql:
        return None

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, email FROM USER WHERE email = %s", email)
    user = cursor.fetchone()
    cursor.close()

    if user:
        return user[0]

    return None

def get_product_by_id(mysql, product_id):
    if not mysql:
        return None

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * from (PRODUCT LEFT JOIN CATEGORY ON PRODUCT.category_id = CATEGORY.id) LEFT JOIN furniture.CONDITION ON PRODUCT.condition_id = furniture.CONDITION.id where PRODUCT.id = %s;", (product_id))
    _product = cursor.fetchone()
    cursor.close()

    if _product:
        print(_product)
        product = Product(_product)
        return product
        
    return None

def get_products(mysql):
    if not mysql:
        return []
    
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * from (PRODUCT LEFT JOIN CATEGORY ON PRODUCT.category_id = CATEGORY.id) LEFT JOIN furniture.CONDITION ON PRODUCT.condition_id = furniture.CONDITION.id;")
    _products = cursor.fetchall()
    cursor.close()

    return [Product(_p) for _p in _products]
   
def search_products(mysql, q):
    if not mysql:
        return []

    try:
        cursor = mysql.get_db().cursor()
        query = "SELECT * from (PRODUCT LEFT JOIN CATEGORY ON PRODUCT.category_id = CATEGORY.id) LEFT JOIN " +\
            "furniture.CONDITION ON PRODUCT.condition_id = furniture.CONDITION.id where PRODUCT.name LIKE '\%%s\%';"
        cursor.execute(query, (q))
        _products = cursor.fetchall()
        cursor.close()
        return [Product(_p) for _p in _products]
    except Exception as err:
        print(err)
    return []

def create_product(mysql, product_details, filename, user_id):
    if not mysql:
        return []

    try:
        cursor = mysql.get_db().cursor()
        query = "INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(query, (product_details.get("name"), product_details.get("price"), product_details.get("condition"), product_details.get("category"), product_details.get("description"), filename, user_id))
        mysql.get_db().commit()
        cursor.close()
        return True
    except Exception as err:
        print(err)
    return False

def get_conditions(mysql):
    if not mysql:
        return []

    try:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM furniture.CONDITION")
        conditions = cursor.fetchall()
        cursor.close()
        return conditions
    except Exception:
        return []

def get_categories(mysql):
    if not mysql:
        return []

    try:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM furniture.CATEGORY")
        categories = cursor.fetchall()
        cursor.close()
        return categories
    except Exception:
        return []