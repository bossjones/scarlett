#!/usr/bin/env python

"""
Scarlett Brain
"""

import scarlett
from scarlett.brain import *
from scarlett.constants import *
from thoonk import Thoonk
from json import loads, dumps

class ScarlettBrainThoonk(ScarlettBrain):

    def __init__(self,name):
      self.config       = scarlett.config
      self.name         = name
      self.redis_host   = self.scarlett.config.get('redis','host')
      self.redis_port   = self.scarlett.config.get('redis','port')
      self.redis_db     = self.scarlett.config.get('redis','db')
      self.thoonk       = Thoonk(host=self.redis_host, port=self.redis_port , db=self.redis_db, listen=self.listen_flag)
      self.listen_flag  = True
      self.pubsub_object = None
      #self.redis_server = redis.Redis(host=self.redis_host, port=self.redis_port , db=self.redis_db)
      #self.redis_server.set("name", "ScarlettBrain")
      ScarlettBrain.__init__(self, self.name)

    def create_brain_feed(self,feed_name,feed_dict={"max_length": 50}):
      if hasattr(self,"self.thoonk"):
         self.thoonk = self.thoonk
      else:
         self.thoonk = self.thoonk().feed(feed_name,feed_dict)

      return self.thoonk

    def get_brain(self):
      return self.thoonk

