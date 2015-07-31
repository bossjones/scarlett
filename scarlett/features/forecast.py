# """
# Defines an interface which all Auth handlers need to implement.
# """

# import scarlett
# from scarlett.features import *
# import forecastio
# import scarlett.basics.voice
# import scarlett.basics.say as scarlett_says

# SCARLETT_ROLE = 'weather'

# class FeatureForecast(Feature):

#     capability = []

#     def __init__(self, voice, brain, *args, **kwargs):
#         self.module_exists("forecastio")
#         super(FeatureForecast, self).__init__(args, kwargs)
#         self._name = "forecastio"
#         self.voice = voice
#         self.brain = brain
#         self.config = scarlett.config
#         self.lat = self.config.get('forecastio', 'lat')
#         self.lng = self.config.get('forecastio', 'lng')
#         self.api_key = self.config.get('forecastio', 'api_key')

#     def add_auth(self, http_request):
#         pass

#     def forecast_play(self):
#         scarlett.basics.voice.play_block('pi-response')
#         forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng)

#         scarlett.log.debug(
#             Fore.YELLOW +
#             "" +
#             forecast.hourly().data[0].temperature)
#         fio_hourly = "%s degrees fahrenheit" % (
#             forecast.hourly().data[0].temperature)
#         fio_hourly = fio_hourly.replace(";", "\;")
#         scarlett_says.say_block(fio_hourly)

#         scarlett.log.debug(Fore.YELLOW + "===========Hourly Data=========")
#         by_hour = forecast.hourly()
#         scarlett.log.debug(
#             Fore.YELLOW +
#             "Hourly Summary: %s" %
#             (by_hour.summary))
#         fio_summary = "Hourly Summary: %s" % (by_hour.summary)
#         fio_summary = fio_summary.replace(";", "\;")
#         scarlett_says.say_block(fio_summary)


#         scarlett.log.debug(Fore.YELLOW + "===========Daily Data=========")
#         by_day = forecast.daily()
#         scarlett.log.debug(
#             Fore.YELLOW +
#             "Daily Summary: %s" %
#             (by_day.summary))
#         fio_day = "Daily Summary: %s" % (by_day.summary)
#         ScarlettTalk.speak(fio_day)
#         self.failed = int(self.brain.set_brain_item_r('scarlett_failed', 0))
#         self.keyword_identified = int(
#             self.brain.set_brain_item_r(
#                 'm_keyword_match',
#                 0))
