from hashlib import sha256

import tornado.web

from backend.firebase_provider.save_message import save_message


class MessageSendHandler(tornado.web.RequestHandler):
    async def post(self):
        message = self.get_argument('message', default=None, strip=False)
        images = self.request.files

        images_tags = None  # backend.ai.get_images_tag()

        message_hash = sha256(message.encode()).hexdigest()

        try:
            save_message(message)
            self.write({'message_hash': message_hash})
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))