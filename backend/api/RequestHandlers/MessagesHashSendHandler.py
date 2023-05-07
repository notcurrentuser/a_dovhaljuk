from hashlib import sha256

import tornado.web

from backend.firebase_provider.save_message import save_message


class MessagesHashSendHandler(tornado.web.RequestHandler):
    async def post(self):
        message_hash = self.get_argument('message_hash', default=None, strip=False)

        message_hash_hash = sha256(message_hash.encode()).hexdigest()

        try:
            save_message('message_hash', message_hash_hash, message_hash)
            self.write({'message_hash_hash': message_hash_hash})
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
