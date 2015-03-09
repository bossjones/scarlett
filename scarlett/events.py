from scarlett.constants import ( EVENT_SCARLETT_START,
                                 EVENT_SCARLETT_STOP,
                                 EVENT_STATE_CHANGED,
                                 EVENT_TIME_CHANGED,
                                 EVENT_CALL_SERVICE,
                                 EVENT_SERVICE_EXECUTED,
                                 EVENT_SERVICE_REGISTER,
                                 EVENT_PLATFORM_DISCOVERED,
                                 EVENT_SCARLETT_SAY,
                                 EVENT_LOCAL,
                                 EVENT_REMOTE
                               )

def scarlett_event(event_type, data=None, origin=EVENT_LOCAL,
    make_dict=False):
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
