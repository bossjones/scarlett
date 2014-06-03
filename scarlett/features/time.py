from features import Feature

class FeatureTime(Feature):

    capability = []

    def __init__(self, host, config, provider):
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
        Feature.__init__(self, "time")

    def add_auth(self, http_request):
        """Invoked to add authentication details to request.

        :type http_request: boto.connection.HTTPRequest
        :param http_request: HTTP request that needs to be authenticated.
        """
        pass
