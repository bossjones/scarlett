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
from subprocess import call
# import urllib
# from urllib import urlencode, urlopen
from scarlett.basics import *
from scarlett.constants import *
import scarlett.basics.voice

class ScarlettTalk(threading.Thread):
    """
    Talk class is a singleton managing TTS for the client
    Some utterance are system (ex : "I'm ready"), and are temporarily generated in /tmp, to limit TTS engine calls
    """
    # Singleton instance
    __instance = None

    # TTS engine enum
    #_engines = type('Enum', (), dict({"pico": 1, "voicerss": 2}))

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Scarlett Talk singleton can't be created twice !")

        # Init thread class
        threading.Thread.__init__(self,brain)
        self._stopevent = threading.Event()
        self.brain = brain
        self.config = scarlett.config
        self.sudo_enabled = self.config.getboolean('speech', 'sudo_enabled')
        self.reading_speed = 165

        self.queue = Queue([])
        self.lang = "en-EN"
        self.engine = "espeak"

        # Start thread
        threading.Thread.start(self)

    def _start(self):
        # Create singleton
        if self.__instance is None:
            self.__instance = ScarlettTalk()

    def _speak(self, msg, block = True):
        # Queue message
        if self.__instance is not None:
            self.__instance.queue.put(msg)

            # Waits the end
            if block == True:
                self.__instance.queue.join()

    def _stop(self):
        # Raise stop event
        if self.__instance is not None:
            self.__instance._stopevent.set()
            self.__instance = None

        # Free gstreamer player
        scarlett.basics.voice.play_free()

    # Export class method
    start = classmethod(_start)
    speak = classmethod(_speak)
    stop = classmethod(_stop)

    def run(self):
        """
        Recorder main loop
        """
        # Thread loop
        while not self._stopevent.isSet():
            # Wait queue
            if self.queue.empty():
                sleep(.1)
                continue

            # Get message
            data = self.queue.get()

            # espeak TTS
            if self.engine == "espeak":
                text = ''.join(e for e in data if e.isalpha() or e.isspace())
                # TODO: Figure out if better to remove shell=True
                call(['/usr/bin/espeak', '-ven+f3', '-k5', '-s150', '"'+ text + '"', '2>&1'])
                #process = subprocess.Popen(['espeak'], stdin=subprocess.PIPE )

            self.queue.task_done()
