import scarlett
from scarlett.constants import *
import threading
import os
import time
import gevent
gevent.monkey.patch_all()
from gevent.socket import wait_read
import redis
import redis.connection
redis.connection.socket = gevent.socket

class ScarlettBase(object):
    """
    Class to route Event communication to all parts of scarlett
    """

    def __init__(self):
      scarlett.set_stream_logger('scarlett')
      scarlett.log.debug(Fore.YELLOW + "Inside ScarlettBase")
      self.config       = scarlett.config
      self.redis_host   = self.scarlett.config.get('redis','host')
      self.redis_port   = self.scarlett.config.get('redis','port')
      self.redis_db     = self.scarlett.config.get('redis','db')
      #self.redis_server = getdb("redis://%s:%i?timeout=%i" % (self.redis_host,self.redis_port,self.redis_db) )
      self.redis_server = redis.Redis(host='localhost',port=6379,db=0)
      self.pubsub       = self.redis_server.pubsub()

    def get_redis_server(self):
        return self.redis_server

    def my_handler(message):
        scarlett.log.debug(Fore.YELLOW + "MY HANDLER" + message['data'])
