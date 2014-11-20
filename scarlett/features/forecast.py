"""
Defines an interface which all Auth handlers need to implement.
"""

import scarlett
from scarlett.features import *
from scarlett.basics import Voice

class FeatureForecast(Feature):

    capability = []

    def __init__(self, voice, **kwargs):
        self.module_exists("forecastio")
        super(FeatureForecast, self).__init__(kwargs)
        self.config             = scarlett.config
        self.lat                = self.config.get('forecastio','lat')
        self.lng                = self.config.get('forecastio','lng')
        self.api_key            = self.config.get('forecastio','api_key')
        self.voice              = Voice()

        #Feature.__init__(self, "forecast")

    def add_auth(self, http_request):
        pass

    def forecast_play(self, cmd):

        self.keyword_identified = 0
        self.voice.play('pi-response')
        forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng)

        scarlett.log.debug(Fore.YELLOW + "" + forecast.hourly().data[0].temperature)
        fio_hourly =  "%s degrees fahrenheit" % (forecast.hourly().data[0].temperature)
        fio_hourly = fio_hourly.replace(";","\;")
        self.voice.speak(fio_hourly)

        scarlett.log.debug(Fore.YELLOW + "===========Hourly Data=========" )
        by_hour = forecast.hourly()
        scarlett.log.debug(Fore.YELLOW + "Hourly Summary: %s" % (by_hour.summary) )
        fio_summary = "Hourly Summary: %s" % (by_hour.summary)
        fio_summary = fio_summary.replace(";","\;")
        self.voice.speak(fio_summary)

        scarlett.log.debug(Fore.YELLOW + "===========Daily Data=========" )
        by_day = forecast.daily()
        scarlett.log.debug(Fore.YELLOW + "Daily Summary: %s" % (by_day.summary))
        fio_day = "Daily Summary: %s" % (by_day.summary)
        self.voice.speak(fio_day)

        return self.keyword_identified
