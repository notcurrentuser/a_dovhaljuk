import pickle
from time import time
from hashlib import sha256

import tornado.web

from backend.firebase_provider.save_message import save_message
from backend.firebase_provider.get_messages import get_messages


class MessagesHashSendHandler(tornado.web.RequestHandler):
    async def post(self):
        message_hash = self.get_argument('message_hash', default=None, strip=False)

        message_hash_hash = sha256(message_hash.encode()).hexdigest()

        try:
            last_item = pickle.dumps(list(get_messages('message_hash', last=1).items())[0])
            prev_message_hash = sha256(last_item).hexdigest()
        except AttributeError:
            prev_message_hash = 'hello world'

        data = {'datetime': time(), 'message_hash': message_hash, 'prev_message_hash': prev_message_hash}

        try:
            save_message('message_hash', message_hash_hash, data)
            self.write({'message_hash_hash': message_hash_hash})
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
