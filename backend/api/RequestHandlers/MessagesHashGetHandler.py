import time
from hashlib import sha256

import tornado.web

from backend.firebase_provider.get_messages import get_messages


class MessagesHashGetHandler(tornado.web.RequestHandler):
    async def post(self):
        hash_id = self.get_argument('hash_id', default=None, strip=False)
        is_last = self.get_argument('is_last', default=None, strip=False)

        try:
            result = get_messages('message_hash', hash_id=hash_id, last=is_last)
            self.write(result)
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
