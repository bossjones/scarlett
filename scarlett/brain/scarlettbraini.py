# -*- coding: UTF-8 -*-

# NOTE: Borrowed a great deal of knowledge from LISA project.

import gobject
gobject.threads_init()

# Imports
import scarlett
import threading
#import os
#import gettext
from Queue import Queue
from time import sleep
import subprocess
from subprocess import call
from scarlett.basics import *
from scarlett.constants import *
import scarlett.basics.voice

import os
import time
import redis
import redis.connection
from json import loads, dumps

import os

# singleton decorator
def singleton(myClass):
    instances = {}
    def getInstance(*args, **kwargs):
      if myClass not in instances:
          instances[myClass] = myClass(*args,**kwargs)
      return instances[myClass]
    return getInstance

@singleton
class ScarlettBrainImproved(redis.Redis):
    """
    Wrapper for Redis pub-sub that uses a pipeline internally
    for buffering message publishing. A thread is run that
    periodically flushes the buffer pipeline.
    """

    def __init__(self, *args, **kwargs):
        super(ScarlettBrainBuffered, self).__init__(*args, **kwargs)
        self.buffer = self.pipeline()
        self.lock = threading.Lock()
        # A factory function that returns a new event object. An event manages a flag that can be set to true with the set() method and reset to false with the clear() method. The wait() method blocks until the flag is true.

        self.config = scarlett.config

        # redis config
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
        self.flush = True

        if self.flush:
            self.wipe_brain()
            self.set_brain_item('m_keyword_match', 0)
            self.set_brain_item('scarlett_successes', 0)
            self.set_brain_item('scarlett_failed', 0)

        thread.start_new_thread(self.flusher, ())

    def flusher(self):
        """
        Thread that periodically flushes the buffer pipeline.
        """
        while True:
            time.sleep(.2)
            with self.lock:
                self.buffer.execute()

    def publish(self, *args, **kwargs):
        """
        Overrides publish to use the buffer pipeline, flushing
        it when the defined buffer size is reached.
        """
        with self.lock:
            self.buffer.publish(*args, **kwargs)
            if len(self.buffer.command_stack) >= 1000:
                self.buffer.execute()
