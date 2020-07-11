"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
#from flask_login import LoginManager
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from database import init_database
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

#login_manager = LoginManager()
#login_manager.init_app(app)
#@login_manager.user_loader
#def load_user(user_id):
    #return User.get(user_id)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

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
                phone = body['phone'],is_active = body['is_active'],deleted = body['deleted'])
        #user.save()
        db.session.add(user)  
        db.session.commit()

        return jsonify(user.serialize()), 200
    else:    
        return 'Some parameters are missing', 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
