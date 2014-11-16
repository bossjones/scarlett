# disabled ########## import scarlett
# disabled ########## from scarlett.constants import *
# disabled ########## import threading
# disabled ########## import os
# disabled ########## import time
# disabled ########## import gevent
# disabled ########## gevent.monkey.patch_all()
# disabled ########## from gevent.socket import wait_read
# disabled ########## import redis
# disabled ########## import redis.connection
# disabled ########## redis.connection.socket = gevent.socket
# disabled ##########
# disabled ########## class ScarlettBase(object):
# disabled ##########     """
# disabled ##########     Class to route Event communication to all parts of scarlett
# disabled ##########     """
# disabled ##########
# disabled ##########     def __init__(self):
# disabled ##########       scarlett.set_stream_logger('scarlett')
# disabled ##########       scarlett.log.debug(Fore.YELLOW + "Inside ScarlettBase")
# disabled ##########       self.config       = scarlett.config
# disabled ##########       self.redis_host   = self.scarlett.config.get('redis','host')
# disabled ##########       self.redis_port   = self.scarlett.config.get('redis','port')
# disabled ##########       self.redis_db     = self.scarlett.config.get('redis','db')
# disabled ##########       #self.redis_server = getdb("redis://%s:%i?timeout=%i" % (self.redis_host,self.redis_port,self.redis_db) )
# disabled ##########       self.redis_server = redis.Redis(host='localhost',port=6379,db=0)
# disabled ##########       self.pubsub       = self.redis_server.pubsub()
# disabled ##########
# disabled ##########     def get_redis_server(self):
# disabled ##########         return self.redis_server
# disabled ##########
# disabled ##########     def my_handler(message):
# disabled ##########         scarlett.log.debug(Fore.YELLOW + "MY HANDLER" + message['data'])
# disabled ##########
