import enum

class ScarlettEventOrigin(enum.Enum):
    """ Check origin of event on bus """

    local = "LOCAL"
    remote = "REMOTE"

    def __str__(self):
        return self.value

def scarlett_event(event_type, data=None, origin=ScarlettEventOrigin.local,make_dict=False):
    """ Returns a dict representation of this Event. """
    if make_dict:
       _data = dict(data)
    else:
       _data = data

    return {
        'event_type': event_type,
        'data': _data,
        'origin': str(origin)
    }
