'''
Created on Jun 26, 2013

@author: peterb
'''
from pkg_resources import resource_filename
import logging
import tornado.ioloop
from tornado.options import options
from puzzled.web.application import Application
from puzzled.web.index_handler import IndexHandler
from puzzled.web.websocket_handler import WebSocketHandler
from puzzled.web.logout_handler import LogoutHandler


def main(port=8080):
    handlers = [
        (r"/", IndexHandler),
        (r"/logout", LogoutHandler),
        (r"/websocket", WebSocketHandler)
    ]
    application = Application(
          handlers,                                          
          template_path=resource_filename('puzzled',"www"),
          static_path=resource_filename('puzzled',"www/static"),
          cookie_secret='puzzled-game-secret',
          cookie_name='puzzled-user',
          debug=True
        )
    application.drop_all_and_create()
    application.listen(port)
    logging.info("listening on port {}".format(port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    options.db_url = "mysql://root:root@127.0.0.1:8889/puzzled?charset=utf8"
    main()