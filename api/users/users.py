from flask import Blueprint, jsonify, request, g
from flask.wrappers import Response
from ..auth.auth import BasicAuthHandler
import db.dao

auth = BasicAuthHandler()
users = Blueprint('users', __name__)

@auth.registerUserHandler
def getUserInfoFromdb(username):
    return db.dao.getPasswordRolesForUser(username)
    

@users.route('/user/<int:id>', methods=['GET'])
def getUser(id):
    return db.dao.getUser(id)



@users.route('/user/', methods=['GET'])
def getAllUsers():
    return db.dao.getAllUsers()

@users.route('/user/', methods=['PUT'])
def createUser():
    data = request.get_json()
    return db.dao.createUser(data['name'], data['displayName'], data['email'], data['phone'], data['password'])

@users.route('/user/update', methods=['POST'])
def updateUser():
    data = request.get_json()
    print(data)
    return db.dao.updateUser(data['name'], data.get('displayName'), data.get('email'), data.get('phone'))

@users.route('/user/<int:id>', methods=['DELETE'])
@auth.require_authentication('Admin')
def deleteUser(id):
    return db.dao.deleteUser(id)


@users.route('/home1/')
@auth.require_authentication()
def home():
    return 'Home Page'

@users.route('/user/current', methods=['POST'])
@auth.require_authentication()
def getCurentUser():
    return db.dao.getUserByName(g.name.decode('utf-8'))

@users.route('/login/', methods=['POST'])
@auth.require_authentication()
def login():
    resp = Response()
    resp.set_cookie("authtoken", g.authtoken)
    return resp




