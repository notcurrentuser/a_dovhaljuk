import asyncio
from threading import Thread

import tornado.web

from RequestHandlers import PrivateKeyGenerationHandler, PrivateKeySignHandler
from RequestHandlers import MessagesSendHandler


class WebServer(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/private_key/generation/", PrivateKeyGenerationHandler.PrivateKeyGenerationHandler),
                    (r"/private_key/sign/", PrivateKeySignHandler.PrivateKeySignHandler),
                    (r"/message/send/", MessagesSendHandler.MessageSendHandler)]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def run(self, port=5465):
        self.listen(port)
        tornado.ioloop.IOLoop.instance().start()


web_server = WebServer()


def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    web_server.run()


thread = Thread(target=start_server, args=())
thread.daemon = True
thread.start()
thread.join()
