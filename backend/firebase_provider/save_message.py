import pyrebase

from backend.settings import FIREBASE_CONFIG

firebase_db = pyrebase.initialize_app(FIREBASE_CONFIG).database()


def save_message(cat: str, hash_id: str, data: str | dict):
    firebase_db.child(cat).child(hash_id).set(data)
