import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.auth.auth import authRequired, AuthnError


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def healthCheck():
    return jsonify({
        'success': True,
        'action': 'Healthy'
    })


@authRequired(permission='get:actors')
@app.route('/actors', methods=['GET'])
def getActors(payload):
    pass


@authRequired(permission='post:actors')
@app.route('/actors', methods=['POST'])
def addActors(payload):
    pass


@authRequired(permission='patch:actors')
@app.route('/actors', methods=['PATCH'])
def updateActors(payload):
    pass


@authRequired(permission='delete:actors')
@app.route('/actors', methods=['DELETE'])
def deleteActors(payload):
    pass


@authRequired(permission='get:movies')
@app.route('/movies', methods=['GET'])
def getMovies(payload):
    pass


@authRequired(permission='post:movies')
@app.route('/movies', methods=['POST'])
def addMovies(payload):
    pass


@authRequired(permission='patch:movies')
@app.route('/movies', methods=['PATCH'])
def updateMovies(payload):
    pass


@authRequired(permission='delete:movies')
@app.route('/movies', methods=['DELETE'])
def deleteMovies(payload):
    pass

