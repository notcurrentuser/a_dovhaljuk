import pyrebase

from backend.settings import FIREBASE_CONFIG

firebase_db = pyrebase.initialize_app(FIREBASE_CONFIG).database()


def get_messages(cat: str, hash_id: str = None, last: int = None):
    result = firebase_db.child(cat)

    if last:
        result = result.order_by_child("datetime").limit_to_last(int(last))
    result = result.get().val()

    if hash_id:
        result = result[hash_id]

    return result
