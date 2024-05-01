# app/__init__.py

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from config import Config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

bootstrap = Bootstrap()
mongo = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))
# mongo = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)

    print(f"MongoDB URI: {app.config['MONGO_URI']}")  # Debug statement

    try:
        mongo.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    from app.routes import main
    app.register_blueprint(main)

    return app


