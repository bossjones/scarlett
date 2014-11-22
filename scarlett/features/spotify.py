import scarlett
from scarlett.features import *


class FeatureSpotify(Feature):

    capability = []

    def __init__(self, **kwargs):
        super(FeatureSpotify, self).__init__(kwargs)
        self._name = "spotify"
        self.voice = voice
        self.brain = brain
        #Feature.__init__(self, "spotify")

    def spotify_play(self, cmd):
        #self.keyword_identified = 0
        self.voice.play('pi-response')
