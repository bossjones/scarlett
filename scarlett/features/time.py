import scarlett
import time
import datetime
from scarlett.features import *

class FeatureTime(Feature):

    capability = []

    def __init__(self,voice):
        self.voice = voice
        self.now = datetime.datetime.now()
        # Today is Saturday, October 18
        Feature.__init__(self, "time")

    def time_play(self,cmd='time'):
      #self.keyword_identified = 0
      self.current_time = self.now.strftime("It is now, %I:%M %p")
      self.current_date = self.now.strftime("Today's date is, %A, %B %d, %Y")
      scarlett.log.debug(Fore.YELLOW + "self.current_time: " + self.current_time)
      scarlett.log.debug(Fore.YELLOW + "self.current_date: " + self.current_date)
      self.voice.speak(self.current_time)
      self.voice.speak(self.current_date)
      return 0
