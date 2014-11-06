#!/usr/bin/env python

"""
Scarlett Brain
"""

from __future__ import unicode_literals
import scarlett
from scarlett.constants import *
import redis
from json import loads, dumps
import threading

class ScarlettBrain(object):

    def __init__(self):
      self.config       = scarlett.config
      self.redis_host   = self.scarlett.config.get('redis','host')
      self.redis_port   = self.scarlett.config.get('redis','port')
      self.redis_db     = self.scarlett.config.get('redis','db')
      self.redis_server = None
      self.pubsub = None
      #self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
      #self.redis_server.set("name", "ScarlettBrain")

    def create_brain(self):
        self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
        self.redis_server.set("name", "ScarlettBrain")
        return self.redis_server

    def get_brain(self):
      return self.redis_server

    def create_brain_event_listener(self):
        if hasattr(self,"self.redis_server"):
           self.pubsub = self.get_brain().pubsub()
        else:
           self.pubsub = self.create_brain().pubsub()

        self.pubsub.subscribe('scarlett-brain')
        thread = p.run_in_thread(sleep_time=0.001)
        self.redis_server.publish('scarlett-brain')

        return self.pubsub

    def get_brain_event_listener(self):
        return self.pubsub

    def sub_brain_event_listener(self):
        return self.create_brain().pubsub()

    def set_keyword_identified(self,keyword_value):
        return self.redis_server.set("keyword_identified", keyword_value)

    def get_keyword_identified(self):
        return self.redis_server.get("keyword_identified")

    def set_brain_item(self,key,value):
        return self.redis_server.set(key, value)

    def get_brain_item(self,key):
        return self.redis_server.get(key)

    def remove_brain_item(self,key):
        return self.redis_server.delete(key)

    def set_service_identified(self,service_name,key):
        return self.redis_server.set("service_%s"%(service_name),service_identified)

    def incr_service_identified(self,service_name):
        return self.redis_server.incr("service_%s"%(service_name))

    def decr_service_identified(self,service_name):
        return self.redis_server.decr("service_%s"%(service_name))

    def get_service_identified(self,service_name):
        return self.redis_server.get("service_%s"%(service_name),service_identified)

    def wipe_brain(self):
      self.redis_server.flushall()

class ScarlettBrainStdnet(object):

    def __init__(self,name):
      self.config       = scarlett.config
      self._name   = name
      self.redis_port   = self.scarlett.config.get('redis','port')
      self.redis_db     = self.scarlett.config.get('redis','db')
      self.redis_server = None
      self.pubsub = None
      #self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
      #self.redis_server.set("name", "ScarlettBrain")

    def create_brain(self):
        self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
        self.redis_server.set("name", "ScarlettBrain")
        return self.redis_server

    def get_brain(self):
      return self.redis_server

    def create_brain_event_listener(self):
        if hasattr(self,"self.redis_server"):
           self.pubsub = self.get_brain().pubsub()
        else:
           self.pubsub = self.create_brain().pubsub()

        self.pubsub.subscribe('scarlett-brain')
        thread = p.run_in_thread(sleep_time=0.001)
        self.redis_server.publish('scarlett-brain')

        return self.pubsub

    def get_brain_event_listener(self):
        return self.pubsub

    def sub_brain_event_listener(self):
        return self.create_brain().pubsub()

    def set_keyword_identified(self,keyword_value):
        return self.redis_server.set("keyword_identified", keyword_value)

    def get_keyword_identified(self):
        return self.redis_server.get("keyword_identified")

    def set_brain_item(self,key,value):
        return self.redis_server.set(key, value)

    def get_brain_item(self,key):
        return self.redis_server.get(key)

    def remove_brain_item(self,key):
        return self.redis_server.delete(key)

    def set_service_identified(self,service_name,key):
        return self.redis_server.set("service_%s"%(service_name),service_identified)

    def incr_service_identified(self,service_name):
        return self.redis_server.incr("service_%s"%(service_name))

    def decr_service_identified(self,service_name):
        return self.redis_server.decr("service_%s"%(service_name))

    def get_service_identified(self,service_name):
        return self.redis_server.get("service_%s"%(service_name),service_identified)

    def wipe_brain(self):
      self.redis_server.flushall()

#   def think(self):
#     if len(self.resp) == 0:
#       return False

# scarlett_config=ScarlettConfig()
#     q = self.resp[0]['utterance']
#     if q in ['nothing', 'cancel', 'no'] or len(q) <= 1:
#       print " * Ignoring", q
#       self.voice.speak("Okay")

#     print " * Thinking about '%s'" % q
#     nq = nltk.pos_tag(nltk.word_tokenize(q))

#     cells = [(cell.test(q, nq), cell) for cell in GreyCell.__subclasses__()]
#     cells = sorted(cells, key=lambda cell: cell[0])
#     score, cell = cells[-1]

#     print " * Cell %s scored %.2f, activating it" % (cell.__name__, score)

#     self.voice.play('pi-response')
#     try:
    @property
    def name(self):
#     except Exception as e:
#       print e
#       self.voice.speak("Something has gone terribly wrong " + self.voice.gimmie('scarlett_owner') + "\! Please try again.")
        return self._name

# class GreyCell(object):
#   @staticmethod
    def __str__(self):

        return "Scarlett Brain name is %s" % (self.name)
