#coding:utf-8
import web

import http_server_host

web.config.debug = False
application = http_server_host.webapp.wsgifunc()
