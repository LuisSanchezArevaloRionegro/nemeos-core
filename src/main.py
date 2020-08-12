"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Form, Workout, Exercise
from flask_login import LoginManager
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

@app.route('/user/create', methods=['POST'])
def add_user():
    body = request.get_json()
    if 'name' not in body:
        return 'please specify name',400
    if 'last_name' not in body:
        return 'please specify last name',400
    if 'email' not in body:
        return 'please specify email', 400
    if 'phone' not in body:
        return 'please specify phone', 400
    if 'password' not in body:
        return 'please specify password', 400
    user = User(name=body['name'], last_name=body['last_name'], email=body['email'], phone=body['phone'], password=body['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/form/create', methods=['POST'])
def add_sign_up_form():
    body = request.get_json()
    if 'age' not in body:
        return 'please specify age',400
    if 'user_id' not in body:
        return 'please specify user id',400
    if 'height' not in body:
        return 'please specify height', 400
    if 'weight' not in body:
        return 'please specify weight', 400
    if 'dedication' not in body:
        return 'please specify dedication', 400
    if 'goal_id' not in body:
        return 'please specify goal id', 400
    form = Form(age=body['age'], user_id=body['user_id'], height=body['height'], weight=body['weight'], dedication=body['dedication'], goal_id=body['goal_id'])
    db.session.add(form)
    db.session.commit()
    return jsonify(form.serialize()), 200

@app.route('/workout/create', methods=['POST'])
def add_workout():
    body = request.get_json()
    if 'age' not in body:
        return 'please specify age',400
    if 'user_id' not in body:
        return 'please specify user id',400
    if 'height' not in body:
        return 'please specify height', 400
    if 'weight' not in body:
        return 'please specify weight', 400
    if 'dedication' not in body:
        return 'please specify dedication', 400
    if 'goal_id' not in body:
        return 'please specify goal id', 400
    form = Form(age=body['age'], user_id=body['user_id'], height=body['height'], weight=body['weight'], dedication=body['dedication'], goal_id=body['goal_id'])
    workout = Workout(age=body['age'], user_id=body['user_id'], height=body['height'], weight=body['weight'], dedication=body['dedication'], goal_id=body['goal_id'])
    db.session.add(form)
    db.session.commit()
    return jsonify(form.serialize()), 200

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200    

@app.route('/exercise/create', methods=['POST'])
def add_exercise():
    body = request.get_json()

    # creating list        
    exercise_list = []   

    if isinstance(body, list):
        for exercise_body in body:
            if 'name' not in exercise_body:
                return 'please specify name',400
            if 'name_en' not in exercise_body:
                return 'please specify name_en',400
            if 'type' not in exercise_body:
                return 'please specify type',400
            exercise = Exercise(name=exercise_body['name'], name_en=exercise_body['name_en'], type=exercise_body['type'])
            exercise_list.append(exercise)
        
        db.session.add_all(exercise_list)
        db.session.commit()
        return jsonify(exercises=[exercise.serialize() for exercise in exercise_list]), 200
    else:
        if 'name' not in body:
            return 'please specify name',400
        if 'name_en' not in body:
            return 'please specify name_en',400
        if 'type' not in body:
            return 'please specify type',400
        
        exercise = Exercise(name=body['name'], name_en=body['name_en'], type=body['type'])
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
