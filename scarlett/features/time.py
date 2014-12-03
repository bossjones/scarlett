import scarlett
import time
import datetime
from scarlett.features import *


class FeatureTime(Feature):

    capability = []

    def __init__(self, voice, brain, *args, **kwargs):
        super(FeatureTime, self).__init__(args,kwargs)
        self._name = "time"
        self.voice = voice
        self.brain = brain
        self.now   = self.set_now()
        # Today is Saturday, October 18
        #Feature.__init__(self, "time")

    def time_play(self, cmd='time'):
        #self.keyword_identified = 0
        self.current_time = self.get_current_time()
        self.current_date = self.get_current_date()
        scarlett.log.debug(
            Fore.YELLOW +
            "self.current_time: " +
            self.current_time)
        scarlett.log.debug(
            Fore.YELLOW +
            "self.current_date: " +
            self.current_date)
        self.voice.speak(self.current_time)
        self.voice.speak(self.current_date)
        return 0

    def get_current_time(self):
        return self.now.strftime("It is now, %I:%M %p")

    def get_current_date(self):
        return self.now.strftime("Today's date is, %A, %B %d, %Y")

    def set_now(self,override=False):
        if override:
            self.now = override
            return override
        return datetime.datetime.now()

    def get_time(self):
        return self.now
