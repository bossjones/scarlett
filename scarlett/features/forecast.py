"""
Defines an interface which all Auth handlers need to implement.
"""

from features import Feature
from scarlett.basics import Voice
import forecastio

class FeatureForecast(Feature):

    capability = []

    def __init__(self, name):
        """Constructs the handlers.
        :type host: string
        :param host: The host to which the request is being sent.

        :type config: boto.pyami.Config
        :param config: Boto configuration.

        :type provider: boto.provider.Provider
        :param provider: Provider details.

        Raises:
            NotReadyToAuthenticate: if this handler is not willing to
                authenticate for the given provider and config.
        """

        ## REFACTOR NEEDED # self.lat                = self.config.get('forecastio','lat')
        ## REFACTOR NEEDED # self.lng                = self.config.get('forecastio','lng')
        ## REFACTOR NEEDED # self.api_key            = self.config.get('forecastio','api_key')

        self.voice = Voice()

        Feature.__init__(self, "forecast")

    def add_auth(self, http_request):
        """Invoked to add authentication details to request.

        :type http_request: boto.connection.HTTPRequest
        :param http_request: HTTP request that needs to be authenticated.
        """
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
