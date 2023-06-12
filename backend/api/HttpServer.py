import asyncio
from threading import Thread

import tornado.web

from .RequestHandlers import PrivateKeyGenerationHandler, PrivateKeySignHandler
from .RequestHandlers import MessagesSendHandler, MessagesGetHandler
from .RequestHandlers import MessagesHashSendHandler, MessagesHashGetHandler


class WebServer(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/private_key/generation/", PrivateKeyGenerationHandler.PrivateKeyGenerationHandler),
            (r"/private_key/sign/", PrivateKeySignHandler.PrivateKeySignHandler),
            (r"/message/send/", MessagesSendHandler.MessageSendHandler),
            (r"/message/get/", MessagesGetHandler.MessagesGetHandler),
            (r"/message_hash/send/", MessagesHashSendHandler.MessagesHashSendHandler),
            (r"/message_hash/get/", MessagesHashGetHandler.MessagesHashGetHandler),
        ]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def run(self):
        # self.listen(int(os.environ.get("PORT", 5000))) #  for heroku
        # self.listen(5465)  # for localhost
        self.listen(8000)  # for azure
        print('backend start')
        tornado.ioloop.IOLoop.instance().start()


web_server = WebServer()


def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    web_server.run()


def run_server():
    thread = Thread(target=start_server, args=())
    thread.daemon = True
    thread.start()
    thread.join()


if __name__ == '__main__':
    run_server()