from flask import Flask, jsonify
from flask_cors import CORS
from app.routes import api

def create_app():
    app=Flask(__name__)
    CORS(app, resources={r'/api/*': {'origins':'*'}})
    app.register_blueprint(api,url_prefix='/api')
    @app.get('/')
    def index(): return jsonify({'name':'Frame Anime Data Studio API','status':'running','health':'/api/health'})
    return app
