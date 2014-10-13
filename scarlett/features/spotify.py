from features import Feature

class FeatureSpotify(Feature):

    capability = []

    def __init__(self, host, config, provider):
        Feature.__init__(self, "spotify")

    def add_auth(self, http_request):
        pass


    def spotify_play(self,cmd):
      self.keyword_identified = 0
      self.voice.play('pi-response')
