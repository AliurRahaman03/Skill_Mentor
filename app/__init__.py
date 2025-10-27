from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

migrate = Migrate()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "12345"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    
    db.init_app(app)
    
    #Blueprints
    from app.routes import auth_routes, skill_routes, ai_routes

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(skill_routes.bp, url_prefix='/skills')
    app.register_blueprint(ai_routes.bp, url_prefix='/ai')


    # Create tables
    with app.app_context():
        db.create_all()

    return app