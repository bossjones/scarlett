import scarlett
import time
from scarlett.features import *
import scarlett.basics.voice


class FeatureTv(Feature):

    capability = []

    def __init__(self, voice, brain, *args, **kwargs):
        super(FeatureTv, self).__init__(args, kwargs)
        self._name = "tv"
        self.time = time
        self.voice = voice
        self.brain = brain

    def add_auth(self, http_request):
        pass

    def tv_play(self, cmd):
        #self.keyword_identified = 0
        self.voice.play('pi-response')
        # REFACTOR # self.arduino.write(cmd)
        self.time.sleep(2)
