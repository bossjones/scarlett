"""
Defines an interface which all Auth handlers need to implement.
"""

from features import Feature
from scarlett.basics import Voice
#import forecastio

class FeatureForecast(Feature):

    capability = []

    def __init__(self, name):
        self.module_exists("forecastio")
        self.config             = scarlett.config
        self.lat                = self.config.get('forecastio','lat')
        self.lng                = self.config.get('forecastio','lng')
        self.api_key            = self.config.get('forecastio','api_key')
        self.voice              = Voice()

        Feature.__init__(self, "forecast")

    def add_auth(self, http_request):
        pass

    def forecast_play(self, cmd):

        self.keyword_identified = 0
        self.voice.play('pi-response')
        forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng)

        print forecast.hourly().data[0].temperature
        fio_hourly =  "%s degrees fahrenheit" % (forecast.hourly().data[0].temperature)
        fio_hourly = fio_hourly.replace(";","\;")
        self.voice.speak(fio_hourly)

        print "===========Hourly Data========="
        by_hour = forecast.hourly()
        print "Hourly Summary: %s" % (by_hour.summary)
        fio_summary = "Hourly Summary: %s" % (by_hour.summary)
        fio_summary = fio_summary.replace(";","\;")
        self.voice.speak(fio_summary)

        print "===========Daily Data========="
        by_day = forecast.daily()
        print "Daily Summary: %s" % (by_day.summary)
        fio_day = "Daily Summary: %s" % (by_day.summary)
        self.voice.speak(fio_day)

        return self.keyword_identified
