# import scarlett
# from scarlett.features import *
# import ystockquote
# import scarlett.basics.voice
# import scarlett.basics.say as scarlett_says


# class FeatureStock(Feature):

#     capability = []

#     def __init__(self, voice, brain, *args, **kwargs):
#         super(FeatureStock, self).__init__(args, kwargs)
#         self._name = "stock"
#         self.voice = voice
#         self.brain = brain
#         self.ystockquote = ystockquote
#         self.stock_price = self.ystockquote.get_price(stock)
#         self.stock_price_string = "%s price is, %f" (stock, self.stock_price)
#         # Today is Saturday, October 18
#         #Feature.__init__(self, "stock")

#     def stock_play(self, stock='ADBE'):
#         scarlett.log.debug(Fore.YELLOW + "" + self.stock_price_string)
#         scarlett_says.say_block(self.stock_price)
#         return 0

#     def get_stock_price(self, stock='ADOBE'):
#         return self.stock_price_string
