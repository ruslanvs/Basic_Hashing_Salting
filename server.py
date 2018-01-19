# basic module:
# import md5
# password = 'password'
# hashed_password = md5.new(password).hexdigest()
# print hashed_password

from flask import Flask, os, binascii
import md5
app = Flask(__name__)
salt = binascii.b2a_hex( os.urandom( 15 ) )

@app.route( "/users/create", methods = ["POST"] )
def create_user():
    username = request.form['username']
    email = request.form['email']
    password = md5.new(request.form['password']).hexdigest()
    insert_query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES ( :username, :email, :password, NOW(), NOW())"
    query_data = { 'username': username, 'email': email, 'password': password }
    mysql.query_db( insert_query, query_data )

@app.route( "/users/login", methods = ["POST"] )
def login_user():
    password = md5.new( request.form['password'] ).hexdigest()
    email = request.form['email']
    user_query = "SELECT * FROM users WHERE users.email = :email AND users.password = :password"
    query_data = { 'email': email, 'password': password }
    user = mysql.query_db( user_query, query_data )

@app.route( "users/nifty_login", methods = ["POST"] )
def nifty_login():
    email = request.form['email']
    password = request.form['password']
    user_query = "SELECT * FROM users WHERE users.email = :email LIMIT 1"
    query_data = { 'email': email }
    user = mysql.query_db( user_query, query_data )
    if len( user ) != 0:
        encrypted_password = md5.new( password + user[0][salt]).hexdigest()
        if user[0]['password'] == encrypted_password:
            pass #successful login
        else:
            pass # invalid password!
    else:
        pass # invalied email!


app.run ( debug = True )