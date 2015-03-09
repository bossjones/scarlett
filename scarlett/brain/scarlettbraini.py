# -*- coding: UTF-8 -*-

# Imports
import scarlett
import thread
import threading
import time
import redis

from scarlett.basics import *
from scarlett.constants import *
import scarlett.basics.voice

import redis.connection
#from scarlett.util import singleton
#from json import loads, dumps

#@singleton
class ScarlettBrainImproved(redis.Redis):
    """
    Wrapper for Redis pub-sub that uses a pipeline internally
    for buffering message publishing. A thread is run that
    periodically flushes the buffer pipeline.

    We can override the following:
    self, host='localhost', port=6379,
                 db=0, password=None, socket_timeout=None,
                 socket_connect_timeout=None,
                 socket_keepalive=None, socket_keepalive_options=None,
                 connection_pool=None, unix_socket_path=None,
                 encoding='utf-8', encoding_errors='strict',
                 charset=None, errors=None,
                 decode_responses=False, retry_on_timeout=False,
                 ssl=False, ssl_keyfile=None, ssl_certfile=None,
                 ssl_cert_reqs=None, ssl_ca_certs=None

    """

    def __init__(self, *args, **kwargs):
        super(ScarlettBrainImproved, self).__init__(*args, **kwargs)
        self.buffer = self.pipeline()
        # A factory function that returns a new primitive lock object.
        # Once a thread has acquired it, subsequent attempts to acquire
        # it block, until it is released; any thread may release it.
        self.lock = threading.Lock()
        # A factory function that returns a new event object.
        # An event manages a flag that can be set to true with the
        # set() method and reset to false with the clear() method.
        # The wait() method blocks until the flag is true.
        #self._stopevent = threading.Event()

        scarlett.log.debug(Fore.YELLOW + "initializing ScarlettBrain")
        self.scarlett_flush = True

        if self.scarlett_flush:
            self.wipe_brain()
            self.set_brain_item('m_keyword_match', 0)
            self.set_brain_item('scarlett_successes', 0)
            self.set_brain_item('scarlett_failed', 0)

        # Start a new thread and return its identifier.
        # The thread executes the function function with the argument
        # list args (which must be a tuple). The optional kwargs
        # argument specifies a dictionary of keyword arguments.
        # When the function returns, the thread silently exits.
        # When the function terminates with an unhandled exception,
        # a stack trace is printed and then the thread exits (but other threads continue to run).
        # thread.start_new_thread(function, args[, kwargs])
        thread.start_new_thread(self.flusher, ())

    def flusher(self):
        """
        Thread that periodically flushes the buffer pipeline.
        """
        while True:
            time.sleep(.2)
            with self.lock:
                # the EXECUTE call sends all buffered commands
                # to the server, returning a list of responses,
                # one for each command.
                self.buffer.execute()

    def publish(self, *args, **kwargs):
        """
        Overrides publish to use the buffer pipeline, flushing
        it when the defined buffer size is reached.
        """
        with self.lock:
            self.buffer.publish(*args, **kwargs)
            if len(self.buffer.command_stack) >= 1000:
                # the EXECUTE call sends all buffered commands
                # to the server, returning a list of responses,
                # one for each command.
                self.buffer.execute()

    # def get_brain(self):
    #     return self

    def set_keyword_identified(self, keyword_value):
        return self.set(
            name="m_keyword_match",
            value=keyword_value)

    def get_keyword_identified(self):
        return self.get(name="m_keyword_match")

    def set_brain_item(self, key, value):
        return self.set(name=key, value=value)

    def set_brain_item_r(self, key, value):
        self.set(name=key, value=value)
        return self.get(name=key)

    def get_brain_item(self, key):
        return self.get(name=key)

    def remove_brain_item(self, key):
        return self.delete(name=key)

    def wipe_brain(self):
        self.flushall()
