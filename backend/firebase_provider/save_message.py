import pyrebase

from backend.settings import FIREBASE_CONFIG

firebase_db = pyrebase.initialize_app(FIREBASE_CONFIG).database()


def save_message(message: str):
    firebase_db.child('message').push(message)
