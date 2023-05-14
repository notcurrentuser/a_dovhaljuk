import base64

import tornado.web
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from backend.firebase_provider.get_messages import get_messages


class MessageDeleteHandler(tornado.web.RequestHandler):
    async def post(self):
        data_hash = self.get_argument('data_hash', default=None, strip=False)
        password_phrase = self.get_argument('password_phrase', default=None, strip=False)
        encrypted_pem_private_key = self.get_argument('encrypted_pem_private_key', default=None, strip=False)

        private_key = serialization.load_pem_private_key(base64.b64decode(encrypted_pem_private_key), bytes(password_phrase, 'utf-8'))

        signature = private_key.sign(
            bytes(data_hash, 'utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        signature = base64.b64encode(signature).decode('utf-8')

        if get_messages('message_hash', hash_id=data_hash):
            pass

        try:
            ...
            # result = get_messages('message', hash_id=hash_id, last=last)
            # self.write(result)
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
