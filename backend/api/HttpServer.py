import asyncio
import os
from threading import Thread

import tornado.web

from RequestHandlers import PrivateKeyGenerationHandler, PrivateKeySignHandler
from RequestHandlers import MessagesSendHandler, MessagesGetHandler, MessageDeleteHandler
from RequestHandlers import MessagesHashSendHandler, MessagesHashGetHandler


class WebServer(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/private_key/generation/", PrivateKeyGenerationHandler.PrivateKeyGenerationHandler),
            (r"/private_key/sign/", PrivateKeySignHandler.PrivateKeySignHandler),
            (r"/message/send/", MessagesSendHandler.MessageSendHandler),
            (r"/message/get/", MessagesGetHandler.MessagesGetHandler),
            (r"/message_hash/send/", MessagesHashSendHandler.MessagesHashSendHandler),
            (r"/message_hash/get/", MessagesHashGetHandler.MessagesHashGetHandler),
            (r"/message/delete/", MessageDeleteHandler.MessageDeleteHandler),
        ]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def run(self):
        self.listen(int(os.environ.get("PORT", 5000)))
        tornado.ioloop.IOLoop.instance().start()


web_server = WebServer()


def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    web_server.run()


thread = Thread(target=start_server, args=())
thread.daemon = True
thread.start()
thread.join()
