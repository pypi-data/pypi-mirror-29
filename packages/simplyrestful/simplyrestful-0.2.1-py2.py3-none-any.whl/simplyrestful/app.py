from flask import Flask, jsonify
from flask_restful import Api
from sqlalchemy.exc import IntegrityError
from simplyrestful.exceptions import NotFound, Conflict


app = Flask(__name__)
api = Api(app)

app.url_map.strict_slashes = False


@app.errorhandler(NotFound)
def not_found_error(e):
    return jsonify(dict(message='Not found', detail=str(e))), 404


@app.errorhandler(Conflict)
def not_found_error(e):
    return jsonify(dict(message='Conflict', detail=str(e))), 409


@app.errorhandler(IntegrityError)
def integrity_error(e):
    return jsonify(dict(message='Integrity error', detail=str(e))), 409


@app.errorhandler(Exception)
def unknown_error(e):
    return jsonify(dict(message='Unknown error', detail=str(e))), 500


@app.teardown_appcontext
def shutdown_session(exception=None):
    from database import session
    session.close()
