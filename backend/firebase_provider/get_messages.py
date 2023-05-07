import pyrebase

from backend.settings import FIREBASE_CONFIG

firebase_db = pyrebase.initialize_app(FIREBASE_CONFIG).database()


def get_messages(cat: str, hash_id: str = None, order_by_datetime=None, order_by_value=None, last: int = None) -> dict:
    result = firebase_db.child(cat)

    if order_by_datetime:
        result = result.order_by_child("datetime")
    elif order_by_value:
        result = result.order_by_value()

    if (order_by_datetime or order_by_value) and last:
        result = result.limit_to_last(int(last))

    result = result.get().val()

    if hash_id:
        result = result[hash_id]

    return result
