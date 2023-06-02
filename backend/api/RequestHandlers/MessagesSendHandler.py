from time import time
from hashlib import sha256

import tornado.web

from backend.firebase_provider.save_message import SaveMessage
from backend.common.text_tags import TextTags

text_tags = TextTags()


class MessageSendHandler(tornado.web.RequestHandler):
    async def post(self):
        save_message = SaveMessage

        message = self.get_argument('message', default=None, strip=False)
        images = self.request.files
        print(images)

        message_hash = sha256(message.encode()).hexdigest()

        images_tags = {'First': 'None'}  # backend.ai.get_images_tag()
        message_description = [i[0] for i in text_tags.get_tags(message)]

        data = {'datetime': time(),
                'message': message,
                'images_tags': images_tags,
                'message_description': message_description
                }

        try:
            save_message.save_message('message', message_hash, data)
            self.write({'message_hash': message_hash})
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
