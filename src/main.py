"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, render_template, redirect
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_login import LoginManager
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from database import init_database
from login_form import LoginForm
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
#from flask_jwt_simple import (
#    JWTManager, jwt_required, create_jwt, get_jwt_identity
#)
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_database()
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

class UserObject:
    def __init__(self, username):
        self.username = username

#@jwt.user_identity_loader
#def user_identity_lookup(user):
#    return user.username        
        

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#Prueba de login
#@app.route('/login', methods=['GET', 'POST'])
#def login(name):
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    #form = LoginForm()
    #if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        #user = User.get_name(name)
        #login_user(user)

        

        #next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        #if not is_safe_url(next):
            #return abort(400)

        #return redirect(next or url_for('index'))
    #return render_template('login.html', form=form)   


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400

    # if password != 'test' or email != 'test':
    #     return jsonify({"msg": "Bad password or email"}), 401

    usercheck = User.query.filter_by(password=password, email=email).first()
    if usercheck == None:
      return jsonify({"msg": "Bad password or email"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



@app.route('/user', methods=['GET'])
def get_users():
    all_users= []
    for user in User.get_all():
        all_users.append(user.serialize())

    return jsonify(all_users)    


@app.route('/user/<email>', methods=['GET'])
def get_user_by_email(email):
    user = User.get_id(email)
    if user:
        return jsonify(user.serialize()), 200
    else:    
        return None, 204


@app.route('/user', methods=['POST'])
def new_user():
    body = request.get_json()
   
    if 'email' in body and 'password' in body:
        user = User(name = body['name'],last_name = body['last_name'],
                email = body['email'], password = body['password'],
                phone = body['phone'],deleted = body['deleted'])
        user.save()
        
        return jsonify(user.serialize()), 200
    else:    
        return 'Some parameters are missing', 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
