# import scarlett
# from scarlett.constants import *
# from stdnet import getdb

# class ScarlettData(object):
#     """ Class to route Event communication to all parts of scarlett """

#     def __init__(self):
#       self.config       = scarlett.config
#       self.redis_host   = self.scarlett.config.get('redis','host')
#       self.redis_port   = self.scarlett.config.get('redis','port')
#       self.redis_db     = self.scarlett.config.get('redis','db')
#       self.redis_server = getdb("redis://%s:%i?timeout=%i" % (self.redis_host,self.redis_port,self.redis_db) )
#       self.pubsub       = None

#     def get_redis_server(self):
#       return self.redis_server
