import scarlett
import ystockquote
from scarlett.features import *

class FeatureStock(Feature):

    capability = []

    def __init__(self,voice):
        self.voice = voice
        self.ystockquote = ystockquote
        # Today is Saturday, October 18
        Feature.__init__(self, "stock")

    def stock_play(self,stock='ADBE'):
      self.stock_price = self.ystockquote.get_price(stock)
      self.stock_price_string = "%s price is, %f" (stock,self.stock_price)
      scarlett.log.debug(Fore.YELLOW + "" + self.stock_price_string)
      self.voice.speak(self.stock_price)
      return 0
