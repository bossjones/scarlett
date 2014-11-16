# DISABLED #### #!/usr/bin/env python
# DISABLED ####
# DISABLED #### """
# DISABLED #### Scarlett Brain
# DISABLED #### """
# DISABLED ####
# DISABLED #### from __future__ import unicode_literals
# DISABLED #### import threading
# DISABLED #### import os
# DISABLED #### import time
# DISABLED #### import gevent
# DISABLED #### from gevent import monkey
# DISABLED #### gevent.monkey.patch_all()
# DISABLED #### import redis
# DISABLED #### import redis.connection
# DISABLED #### redis.connection.socket = gevent.socket
# DISABLED #### import scarlett
# DISABLED #### from scarlett.constants import *
# DISABLED #### import redis
# DISABLED #### from json import loads, dumps
# DISABLED ####
# DISABLED #### class ScarlettBrain(object):
# DISABLED ####
# DISABLED ####     def __init__(self):
# DISABLED ####       self.config       = scarlett.config
# DISABLED ####       self.redis_host   = self.scarlett.config.get('redis','host')
# DISABLED ####       self.redis_port   = self.scarlett.config.get('redis','port')
# DISABLED ####       self.redis_db     = self.scarlett.config.get('redis','db')
# DISABLED ####       self.redis_server = None
# DISABLED ####       self.pubsub = None
# DISABLED ####       scarlett.log.debug(Fore.YELLOW + "initializing ScarlettBrain")
# DISABLED ####       #self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
# DISABLED ####       #self.redis_server.set("name", "ScarlettBrain")
# DISABLED ####
# DISABLED ####     def create_brain(self):
# DISABLED ####         self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
# DISABLED ####         self.redis_server.set("name", "ScarlettBrain")
# DISABLED ####         scarlett.log.debug(Fore.YELLOW + "create_brain")
# DISABLED ####         return self.redis_server
# DISABLED ####
# DISABLED ####     def get_brain(self):
# DISABLED ####       return self.redis_server
# DISABLED ####
# DISABLED ####     #def create_brain_event_listener(self):
# DISABLED ####     #    if hasattr(self,"self.redis_server"):
# DISABLED ####     #       self.pubsub = self.get_brain().pubsub()
# DISABLED ####     #    else:
# DISABLED ####     #       self.pubsub = self.create_brain().pubsub()
# DISABLED #### #
# DISABLED ####     #    self.pubsub.subscribe('scarlett-brain')
# DISABLED ####     #    thread = p.run_in_thread(sleep_time=0.001)
# DISABLED ####     #    self.redis_server.publish('scarlett-brain')
# DISABLED #### #
# DISABLED ####     #    return self.pubsub
# DISABLED ####
# DISABLED ####     def get_brain_event_listener(self):
# DISABLED ####         return self.pubsub
# DISABLED ####
# DISABLED ####     def sub_brain_event_listener(self):
# DISABLED ####         return self.create_brain().pubsub()
# DISABLED ####
# DISABLED ####     def set_keyword_identified(self,keyword_value):
# DISABLED ####         return self.redis_server.set("keyword_identified", keyword_value)
# DISABLED ####
# DISABLED ####     def get_keyword_identified(self):
# DISABLED ####         return self.redis_server.get("keyword_identified")
# DISABLED ####
# DISABLED ####     def set_brain_item(self,key,value):
# DISABLED ####         return self.redis_server.set(key, value)
# DISABLED ####
# DISABLED ####     def get_brain_item(self,key):
# DISABLED ####         return self.redis_server.get(key)
# DISABLED ####
# DISABLED ####     def remove_brain_item(self,key):
# DISABLED ####         return self.redis_server.delete(key)
# DISABLED ####
# DISABLED ####     def set_service_identified(self,service_name,key):
# DISABLED ####         return self.redis_server.set("service_%s"%(service_name),service_identified)
# DISABLED ####
# DISABLED ####     def incr_service_identified(self,service_name):
# DISABLED ####         return self.redis_server.incr("service_%s"%(service_name))
# DISABLED ####
# DISABLED ####     def decr_service_identified(self,service_name):
# DISABLED ####         return self.redis_server.decr("service_%s"%(service_name))
# DISABLED ####
# DISABLED ####     def get_service_identified(self,service_name):
# DISABLED ####         return self.redis_server.get("service_%s"%(service_name),service_identified)
# DISABLED ####
# DISABLED ####     def wipe_brain(self):
# DISABLED ####       self.redis_server.flushall()
# DISABLED ####
# DISABLED ####     def start_subscriber():
# DISABLED ####         crongreenlet = gevent.spawn(cron)
# DISABLED ####
# DISABLED ####     def cron():
# DISABLED ####         while True:
# DISABLED ####             scarlett.log.debug(Fore.YELLOW + "Hello from cron greenlet.")
# DISABLED ####             gevent.sleep(0.2)

    # @property
    # def name(self):
    #     return self._name

    # def __str__(self):
    #     return "Scarlett Brain name is %s" % (self.name)



# class ScarlettBrainStdnet(object):

#     def __init__(self,name):
#       self.config       = scarlett.config
#       self._name   = name
#       self.redis_port   = self.scarlett.config.get('redis','port')
#       self.redis_db     = self.scarlett.config.get('redis','db')
#       self.redis_server = None
#       self.pubsub = None
#       #self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
#       #self.redis_server.set("name", "ScarlettBrain")

#     def create_brain(self):
#         self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
#         self.redis_server.set("name", "ScarlettBrain")
#         return self.redis_server

#     def get_brain(self):
#       return self.redis_server

#     def create_brain_event_listener(self):
#         if hasattr(self,"self.redis_server"):
#            self.pubsub = self.get_brain().pubsub()
#         else:
#            self.pubsub = self.create_brain().pubsub()

#         self.pubsub.subscribe('scarlett-brain')
#         thread = p.run_in_thread(sleep_time=0.001)
#         self.redis_server.publish('scarlett-brain')

#         return self.pubsub

#     def get_brain_event_listener(self):
#         return self.pubsub

#     def sub_brain_event_listener(self):
#         return self.create_brain().pubsub()

#     def set_keyword_identified(self,keyword_value):
#         return self.redis_server.set("keyword_identified", keyword_value)

#     def get_keyword_identified(self):
#         return self.redis_server.get("keyword_identified")

#     def set_brain_item(self,key,value):
#         return self.redis_server.set(key, value)

#     def get_brain_item(self,key):
#         return self.redis_server.get(key)

#     def remove_brain_item(self,key):
#         return self.redis_server.delete(key)

#     def set_service_identified(self,service_name,key):
#         return self.redis_server.set("service_%s"%(service_name),service_identified)

#     def incr_service_identified(self,service_name):
#         return self.redis_server.incr("service_%s"%(service_name))

#     def decr_service_identified(self,service_name):
#         return self.redis_server.decr("service_%s"%(service_name))

#     def get_service_identified(self,service_name):
#         return self.redis_server.get("service_%s"%(service_name),service_identified)

#     def wipe_brain(self):
#       self.redis_server.flushall()

# #   def think(self):
# #     if len(self.resp) == 0:
# #       return False

# # scarlett_config=ScarlettConfig()
# #     q = self.resp[0]['utterance']
# #     if q in ['nothing', 'cancel', 'no'] or len(q) <= 1:
# #       print " * Ignoring", q
# #       self.voice.speak("Okay")

# #     print " * Thinking about '%s'" % q
# #     nq = nltk.pos_tag(nltk.word_tokenize(q))

# #     cells = [(cell.test(q, nq), cell) for cell in GreyCell.__subclasses__()]
# #     cells = sorted(cells, key=lambda cell: cell[0])
# #     score, cell = cells[-1]

# #     print " * Cell %s scored %.2f, activating it" % (cell.__name__, score)

# #     self.voice.play('pi-response')
# #     try:
#     @property
#     def name(self):
# #     except Exception as e:
# #       print e
# #       self.voice.speak("Something has gone terribly wrong " + self.voice.gimmie('scarlett_owner') + "\! Please try again.")
#         return self._name

# # class GreyCell(object):
# #   @staticmethod
#     def __str__(self):

#         return "Scarlett Brain name is %s" % (self.name)
