import base64

import tornado.web
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class PrivateKeySignHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, '
                        'Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def options(self):
        pass

    async def post(self):
        password_phrase = self.get_argument('password_phrase', default=None, strip=False)
        data_hash = self.get_argument('data_hash', default=None, strip=False)
        encrypted_pem_private_key = self.get_argument('encrypted_pem_private_key', default=None, strip=False)

        private_key = serialization.load_pem_private_key(base64.b64decode(encrypted_pem_private_key), bytes(password_phrase, 'utf-8'))

        data_hash = bytes(data_hash, 'utf-8')

        signature = private_key.sign(
            data_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )


        try:
            self.write({'signature': base64.b64encode(signature).decode('utf-8')})
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
