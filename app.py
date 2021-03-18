import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({
            'success': True,
            'action': 'HelloWorld'
        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)