'''
Created on Jun 26, 2013

@author: peterb
'''
from pkg_resources import resource_filename
import tornado.ioloop
from puzzled.web.application import Application
from puzzled.web.index_handler import IndexHandler
from puzzled.web.websocket_handler import WebSocketHandler
import logging


def main(port=8080):
    application = Application([
        (r"/", IndexHandler),
        (r"/websocket", WebSocketHandler)
        ],                                          
          template_path=resource_filename('puzzled',"www"),
          static_path=resource_filename('puzzled',"www/static"),
          cookie_secret='puzzled-game-secret',
          cookie_name='puzzled-user',
          debug=True
        )
    application.listen(port)
    logging.info("listening on port {}".format(port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()