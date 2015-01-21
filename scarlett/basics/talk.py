# -*- coding: UTF-8 -*-

# NOTE: Borrowed a great deal of knowledge from LISA project.

import gobject
gobject.threads_init()

# Imports
import scarlett
import threading
import os
import gettext
from Queue import Queue
from time import sleep
from subprocess import call
# import urllib
# from urllib import urlencode, urlopen
from random import randint
# from twisted.python import log
from scarlett.basics import *
from scarlett.constants import *
import scarlett.basics.voice

# System utterance definition : key : {(weight1, message1), (weight2, message2)}
# Talk will randomly choose a message in list, balanced by weights
#### DISABLED # _utterances = {
#### DISABLED #     'yes':             {(5, _("Yes ?")),
#### DISABLED #                         (1, _("I'm listening"))
#### DISABLED #                        },
#### DISABLED #     'error_conf':      {(1, _("My configuration file is not readable")),
#### DISABLED #                         (1, _("There's an error with my configuration file"))
#### DISABLED #                        },
#### DISABLED #     'not_understood':  {(1, _("I didn't understand your question")),
#### DISABLED #                         (1, _("I can't hear you clearly")),
#### DISABLED #                         (1, _("I didn't understand"))
#### DISABLED #                        },
#### DISABLED #     'please_repeat':   {(1, _("Can you repeat please ?")),
#### DISABLED #                         (1, _("I didn't understand, can you repeat please ?"))
#### DISABLED #                        },
#### DISABLED #     'ready':           {(3, _("I'm ready ok")),
#### DISABLED #                         (1, _("Initialization completed")),
#### DISABLED #                         (1, _("I'm ready to answer your questions"))
#### DISABLED #                        },
#### DISABLED #     'no_server':       {(1, _("Sorry, I can't connect to the server")),
#### DISABLED #                         (1, _("I can't join the server, please check your connection"))
#### DISABLED #                        },
#### DISABLED #     'lost_server':     {(1, _("An error happened, I'm not available anymore")),
#### DISABLED #                         (1, _("My connection was interrupted, please wait"))
#### DISABLED #                        }
#### DISABLED #     }

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

        #self.configuration = ConfigManagerSingleton.get().getConfiguration()

        self.queue = Queue([])
        self.lang = "en-EN"
        self.engine = "espeak"

        # if self.configuration.has_key('lang'):
        #     self.lang = self.configuration['lang']
        # if self.configuration.has_key("tts") == False or self.configuration["tts"].lower() == "pico"or self.configuration["tts"].lower() == "picotts":
        #     self.engine = "pico"
        #     self.ext = "wav"
        # elif self.configuration["tts"].lower() == "voicerss" and "voicerss_key" in self.configuration:
        #     self.engine = "voicerss"
        #     self.ext = "ogg"
        #     self.voicerss_key = self.configuration["voicerss_key"]
        # else:
        #     player.play_block("error_conf")
        #     return

        # Init pre-synthetized utterances
        #self._init_sys_utterance()

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
            filename = soundpath + soundfile + "." + self.ext

            # # System utterances
            # if _utterances.has_key(data):
            #     # Randomize a weight
            #     weight = randint(1, sum((msg[0] for msg in _utterances[data])))
            #     for i, msg in enumerate(_utterances[data]):
            #         weight = weight - msg[0]
            #         if weight <= 0:
            #             break

            #     # Create filename
            #     filename = "%s%s_%s_%d.%s" % (soundpath, self.engine, data, i, self.ext.lower())

            # espeak TTS
            if self.engine == "espeak":
                text = ''.join(e for e in data if e.isalpha() or e.isspace())
                # TODO: Figure out if better to remove shell=True
                call(['/usr/bin/espeak', '-ven+f3', '-k5', '-s150', '"'+ text + '"', '2>&1'])
                #process = subprocess.Popen(['espeak'], stdin=subprocess.PIPE )

            # # Play synthetized file
            # if os.path.exists(filename):
            #     log.msg(_("Playing generated TTS").encode('utf8'))
            #     player.play_block(sound = filename, path = soundpath, ext = self.ext)
            # else:
            #     log.msg(_("There was an error creating the output file %(filename)s" % {'filename': str(filename)}).encode('utf8'))

            # Remove message from queue
            self.queue.task_done()

    # def _init_sys_utterance(self):
    #     """
    #     Generate system utterance
    #     """
    #     for utt in _utterances:
    #         for i, msg in enumerate(_utterances[utt]):
    #             filename = "%s%s_%s_%d.%s" % (soundpath, self.engine, utt, i, self.ext.lower())

    #             # If already generated
    #             if os.path.isfile(filename):
    #                 os.remove(filename)

    #             log.msg(_("Generating %(filename)s : '%(message)s'" % {'filename': str(filename), 'message': msg[1]}).encode('utf8'))

    #             # VoiceRSS
    #             if self.engine == "voicerss":
    #                 urllib.urlretrieve("http://api.voicerss.org/?%s" % urllib.urlencode({"c": self.ext.upper(),
    #                                                                                      "r": 1,
    #                                                                                      "f": "16khz_16bit_mono",
    #                                                                                      "key": "03e60c7e670b405f9210cd025c2bb440",
    #                                                                                      "src": msg[1],
    #                                                                                      "hl": self.lang}), filename)

    #             # PicoTTS
    #             elif self.engine == "pico" and not os.path.isfile(filename):
    #                 call(['/usr/bin/pico2wave', '-w', filename, '-l', self.lang, '"'+ msg[1] + '"'])


### DISABLE #    def __init__(self, brain):
### DISABLE #        super(Voice, self).__init__(brain)
### DISABLE #        self.brain = brain
### DISABLE #        self.config = scarlett.config
### DISABLE #        self.sudo_enabled = self.config.getboolean('speech', 'sudo_enabled')
### DISABLE #        self.reading_speed = 165
### DISABLE #
### DISABLE #    # best sounding female voice: espeak -ven+f3 -k5 -s150 "hello malcolm"
### DISABLE #    def speak(self, text, speed=150):
### DISABLE #        text = ''.join(e for e in text if e.isalpha() or e.isspace())
### DISABLE #        if self.sudo_enabled:
### DISABLE #            subprocess.Popen('sudo espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text), shell=True).wait()
### DISABLE #        else:
### DISABLE #            subprocess.Popen('espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text), shell=True).wait()
### DISABLE #
### DISABLE #    def greetings_play(self):
### DISABLE #        self.speak(
### DISABLE #            "Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands")
### DISABLE #
### DISABLE #    def read(self, text):
### DISABLE #        self.speak(text, self.reading_speed)
