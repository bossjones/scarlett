import scarlett
import time
from features import *

class FeatureTime(Feature):

    capability = []

    def __init__(self, host, config, provider):
        self.time = time
        Feature.__init__(self, "time")

    def add_auth(self, http_request):
        pass

    def time_play(self,cmd):
      #### REFACTOR pi_time = pi.TimeNow().activate(self,"dont matter","dont matter")
      self.voice.speak("YOU KNOW WHAT TIME IT IS RIGHT NOW HOME BOY")
      self.keyword_identified = 0
      self.voice.play('pi-response')
