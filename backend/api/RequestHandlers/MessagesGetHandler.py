import tornado.web

from backend.firebase_provider.get_messages import get_messages


class MessagesGetHandler(tornado.web.RequestHandler):
    async def post(self):
        order_by_value = self.get_argument('order_by_value', default=None, strip=False)
        last = self.get_argument('last', default=None, strip=False)

        try:
            result = get_messages('message', last=last, order_by_value=order_by_value)
            self.write(result)
        except Exception as e:
            raise tornado.web.HTTPError(status_code=500, log_message=str(e))
