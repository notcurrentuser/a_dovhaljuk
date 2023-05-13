import tornado.web

from backend.firebase_provider.get_messages import get_messages


class MessagesGetHandler(tornado.web.RequestHandler):
    async def get(self):
        hash_id = self.get_argument('hash_id', default=None, strip=False)
        last = self.get_argument('last', default=None, strip=False)

        try:
            result = get_messages('message', hash_id=hash_id, last=last)
            self.write(result)
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
