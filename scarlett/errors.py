class ScarlettError(Exception):
    pass


class ConnectionError(ScarlettError):
    pass


class ServerUnavailable(ScarlettError):
    pass


class ProtocolError(ScarlettError):
    pass


class UnknownCommandError(ScarlettError):
    pass


class ExceededConnectionAttempts(ScarlettError):
    pass


class InvalidClientState(ScarlettError):
    pass


class InvalidWorkerState(ScarlettError):
    pass


class InvalidAdminClientState(ScarlettError):
    pass
