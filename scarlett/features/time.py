import scarlett
import time
import datetime
from scarlett.features import *
import scarlett.basics.voice
from scarlett.basics.talk import ScarlettTalk
import scarlett.basics.say as scarlett_says

class FeatureTime(Feature):

    capability = []

    def __init__(self, voice, brain, *args, **kwargs):
        super(FeatureTime, self).__init__(args, kwargs)
        self._name = "time"
        self.voice = voice
        self.brain = brain
        self.now = self.set_now()

    def time_play(self, cmd='time'):
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

        scarlett_says.say_block(self.current_time)
        scarlett_says.say_block(self.current_date)
        self.failed = int(self.brain.set_brain_item_r('scarlett_failed', 0))
        self.keyword_identified = int(
            self.brain.set_brain_item_r(
                'm_keyword_match',
                0))

    def get_current_time(self):
        return self.now.strftime("It is now, %I:%M %p")

    def get_current_date(self):
        return self.now.strftime("Today's date is, %A, %B %d, %Y")

    def set_now(self, override=False):
        if override:
            self.now = override
            return override
        return datetime.datetime.now()

    def get_time(self):
        return self.now
