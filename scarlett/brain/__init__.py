#!/usr/bin/env python

"""
Scarlett Brain

"""

#from __future__ import unicode_literals
import os
import time
import redis
import redis.connection
import scarlett
from scarlett.constants import *
from json import loads, dumps


class ScarlettBrain(object):

    _global_states = []

    def __init__(self, brain_name, flush=True, **kwargs):
        self.brain_name = brain_name
        self.config = scarlett.config
        self.redis_host = scarlett.config.get('redis', 'host')
        self.redis_port = scarlett.config.get('redis', 'port')
        self.redis_db = scarlett.config.get('redis', 'db')
        self.redis_server = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db)
        self.brain_sub = redis.client.Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db)
        scarlett.log.debug(Fore.YELLOW + "initializing ScarlettBrain")
        self.redis_server.set("name", "ScarlettBrain")

        if flush:
            self.wipe_brain()
            self.set_brain_item('scarlett_main_keyword_identified',0)
            self.set_brain_item('scarlett_successes',0)
            self.set_brain_item('scarlett_failed',0)

    def get_brain(self):
        return self.redis_server

    def brain_publish(self, channel_name, **kwargs):
        return self.redis_server(channel_name, data)

    def get_brain_event_listener(self):
        return self.brain_sub

    def set_keyword_identified(self, keyword_value):
        return self.redis_server.set(
            "scarlett_main_keyword_identified",
            keyword_value)

    def get_keyword_identified(self):
        return self.redis_server.get("scarlett_main_keyword_identified")

    def set_brain_item(self, key, value):
        return self.redis_server.set(key, value)

    def set_brain_item_r(self, key, value):
        self.redis_server.set(key, value)
        return self.redis_server.get(key)

    def get_brain_item(self, key):
        return self.redis_server.get(key)

    def remove_brain_item(self, key):
        return self.redis_server.delete(key)

    def set_service_identified(self, service_name, key):
        return self.redis_server.set(
            "service_%s" %
            (service_name),
            service_identified)

    def incr_service_identified(self, service_name):
        return self.redis_server.incr("service_%s" % (service_name))

    def decr_service_identified(self, service_name):
        return self.redis_server.decr("service_%s" % (service_name))

    def get_service_identified(self, service_name):
        return self.redis_server.get(
            "service_%s" %
            (service_name),
            service_identified)

    def wipe_brain(self):
        self.redis_server.flushall()
