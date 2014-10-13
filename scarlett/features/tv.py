from features import Feature

class FeatureTv(Feature):

    capability = []

    def __init__(self, host, config, provider):
        Feature.__init__(self, "tv")

    def add_auth(self, http_request):
        pass

    def tv_play(self,cmd):
      self.keyword_identified = 0
      self.voice.play('pi-response')
      #### REFACTOR # self.arduino.write(cmd)
      self.time.sleep(2)

