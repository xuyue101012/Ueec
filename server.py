#!/usr/bin/env python
# coding=utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
import redis
from application import application


from tornado.options import define, options

define("port", default = 8300, help = "run on the given port", type = int)
# 清空redis中的所有数据，每次重启时运行一次即可
def clean_redis():
	r.flushdb()
# 初始化redis连接并赋值给一个对象，以供全局调用
r = redis.Redis(host="127.0.0.1", port=6379,db=0)
def main():
    #clean_redis()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print "Development server is running at http://127.0.0.1:%s" % options.port
    print "Quit the server with Control-C"

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
