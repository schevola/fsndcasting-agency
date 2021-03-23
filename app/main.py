import sys

from flask import Flask, request, abort, jsonify
from sqlalchemy.exc import IntegrityError

from app.auth.auth import authRequired, AuthnError
from app.database.models import setup_db, Actor, Movie


app = Flask(__name__)
setup_db(app)


@app.route('/', methods=['GET'])
def healthCheck():
    return jsonify({
        'success': True,
        'action': 'Healthy'
    })


@app.route('/actors', methods=['GET'])
@authRequired(permission='get:actors')
def getActors(payload):
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
    except IntegrityError:
        abort(409)
    return jsonify({
        'success': True,
        'actor': newActor.toString()
    })


@app.route('/actors/<int:actorId>', methods=['PATCH'])
@authRequired(permission='patch:actors')
def updateActors(payload, actorId):
    requestBody = request.json
    actor = Actor.query.get(actorId)
    if actor is None:
        abort(404)
    if 'name' in requestBody.keys():
        actor.name = requestBody['name']
    if 'age' in requestBody.keys():
        actor.age = requestBody['age']
    if 'gender' in requestBody.keys():
        actor.gender = requestBody['gender']
    try:
        actor.update()
    except IntegrityError:
        abort(409)
    return jsonify({
        'success': True,
        'actor': actor.toString()
    })


@app.route('/actors/<int:actorId>', methods=['DELETE'])
@authRequired(permission='delete:actors')
def deleteActors(payload, actorId):
    actor = Actor.query.get(actorId)
    if actor is None:
        abort(404)
    try:
        actor.delete()
    except IntegrityError:
        abort(409)
    return jsonify({
        'success': True,
        'actorId': actorId
    })


@app.route('/movies', methods=['GET'])
@authRequired(permission='get:movies')
def getMovies(payload):
    movies = Movie.query.all()
    return jsonify({
        'success': True,
        'movies': [movie.toString() for movie in movies]
    })


@app.route('/movies', methods=['POST'])
@authRequired(permission='post:movies')
def addMovies(payload):
    requestBody = request.json
    validateMovieBody(requestBody)
    newMovie = Movie()
    newMovie.title = requestBody['title']
    newMovie.releaseDate = requestBody['releaseDate']
    try:
        newMovie.add()
    except IntegrityError:
        abort(409)
    return jsonify({
        'success': True,
        'movie': newMovie.toString()
    })


@app.route('/movies/<int:movieId>', methods=['PATCH'])
@authRequired(permission='patch:movies')
def updateMovies(payload, movieId):
    requestBody = request.json
    movie = Movie.query.get(movieId)
    if movie is None:
        abort(404)
    if 'title' in requestBody.keys():
        movie.title = requestBody['title']
    if 'releaseDate' in requestBody.keys():
        movie.releaseDate = requestBody['releaseDate']
    try:
        movie.update()
    except IntegrityError:
        abort(409)
    return jsonify({
        'success': True,
        'movie': movie.toString()
    })


@app.route('/movies/<int:movieId>', methods=['DELETE'])
@authRequired(permission='delete:movies')
def deleteMovies(payload, movieId):
    movie = Movie.query.get(movieId)
    if None is movie:
        abort(404)
    try:
        movie.delete()
    except IntegrityError:
        abort(409)
    return jsonify({
        'success': True,
        'movieId': movieId
    })


def validateActorBody(body):
    if "name" not in body.keys() or "age" not in body.keys() or \
            "gender" not in body.keys():
        abort(400)


def validateMovieBody(body):
    if "title" not in body.keys() or "releaseDate" not in body.keys():
        abort(400)


@app.errorhandler(AuthnError)
def auth_error_handler(auth_error):
    return jsonify({
        "success": False,
        "errorCode": auth_error.error['code']
    }), 401


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


@app.errorhandler(404)
def databaseError(error):
    return jsonify({
        "success": False,
        "errorCode": "Resource Not Found"
    }), 404


@app.errorhandler(401)
def unAuthorized(error):
    return jsonify({
        "success": False,
        "errorCode": "Authorization Required"
    }), 401
