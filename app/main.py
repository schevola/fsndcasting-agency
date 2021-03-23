import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.auth.auth import authRequired, AuthnError
from app.database.models import setup_db, Actor, Movie


app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/', methods=['GET'])
def healthCheck():
    return jsonify({
        'success': True,
        'action': 'Healthy'
    })



@app.route('/actors', methods=['GET'])
@authRequired(permission='get:actors')
def getActors(payload):
    print("getting actors")
    actors = Actor.query.all()
    return jsonify({
        'success': True,
        'actors': [actor.toString() for actor in actors]
    })



@app.route('/actors', methods=['POST'])
@authRequired(permission='post:actors')
def addActors(payload):
    requestBody = request.json
    validateActorBody(requestBody)
    newActor = Actor()
    newActor.name = requestBody['name']
    newActor.age = requestBody['age']
    newActor.gender = requestBody['gender']
    try:
        newActor.add()
    except:
        abort(409)
    return jsonify({
        'success': True,
        'actor': newActor.toString()
    })



@app.route('/actors', methods=['PATCH'])
@authRequired(permission='patch:actors')
def updateActors(payload):
    pass



@app.route('/actors', methods=['DELETE'])
@authRequired(permission='delete:actors')
def deleteActors(payload):
    pass



@app.route('/movies', methods=['GET'])
@authRequired(permission='get:movies')
def getMovies(payload):
    pass


@app.route('/movies', methods=['POST'])
@authRequired(permission='post:movies')
def addMovies(payload):
    pass



@app.route('/movies', methods=['PATCH'])
@authRequired(permission='patch:movies')
def updateMovies(payload):
    pass



@app.route('/movies', methods=['DELETE'])
@authRequired(permission='delete:movies')
def deleteMovies(payload):
    pass

def validateActorBody(body):
    if "name" not in body.keys() or "age" not in body.keys() or "gender" not in body.keys():
        abort(400)







@app.errorhandler(409)
def databaseError(error):
    return jsonify({
        "success": False,
        "errorCode": "DataBase insert error"
    }), 409

@app.errorhandler(400)
def databaseError(error):
    return jsonify({
        "success": False,
        "errorCode": "Invalid Request"
    }), 400
