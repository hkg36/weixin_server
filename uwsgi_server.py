#coding:utf-8
import web

import http_server_host

webapp=web.application(http_server_host.urls, globals())
web.config.debug = False
application = webapp.wsgifunc()
