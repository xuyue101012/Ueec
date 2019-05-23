#!/usr/bin/env python
# coding=utf-8

from url import url

import tornado.web
import os

settings = dict(
	static_path = os.path.join(os.path.dirname(__file__), "statics"),
	cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
	login_url = '/',
	redis={
		'host':'127.0.0.1',
		'port':6379,
		'db':0
	}
    )

application = tornado.web.Application(
    handlers = url,
    **settings
    )
