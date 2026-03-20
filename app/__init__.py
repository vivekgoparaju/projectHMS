from flask import Flask
from flask_session import Session

def create_app():
    app=Flask(__name__)

    app.config['secret_key']='c0ff3df8-211a-11f1-a587-80000b2f460c'
    app.config['SESSION_TYPE']='filesystem'
    app.config['SESSION_PERMANENT']=True
    Session(app)
    # REGISTER BLUREPRINTS
    from .patient import patient
    app.register_blueprint(patient, url_prefix='/patient')
        
    return app