import base64

import tornado.web
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class PrivateKeyGenerationHandler(tornado.web.RequestHandler):
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

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        encrypted_pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(bytes(password_phrase, 'utf-8'))
        )

        pem_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        try:
            self.write({'encrypted_pem_private_key': base64.b64encode(encrypted_pem_private_key).decode('utf-8'),
                        'pem_public_key': base64.b64encode(pem_public_key).decode('utf-8')})
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
