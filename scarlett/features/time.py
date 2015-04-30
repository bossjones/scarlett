import scarlett
import time
import datetime
from scarlett.features import *
#import scarlett.basics.voice
#import scarlett.basics.say as scarlett_says

import gobject

import dbus
import dbus.service

from scarlett.events import scarlett_event

from scarlett.constants import ( EVENT_SCARLETT_START,
                                 EVENT_SCARLETT_STOP,
                                 EVENT_STATE_CHANGED,
                                 EVENT_TIME_CHANGED,
                                 EVENT_CALL_SERVICE,
                                 EVENT_SERVICE_EXECUTED,
                                 EVENT_SERVICE_REGISTER,
                                 EVENT_PLATFORM_DISCOVERED,
                                 EVENT_SCARLETT_SAY,
                                 EVENT_BRAIN_UPDATE,
                                 EVENT_BRAIN_CHECK
                               )

SCARLETT_FEATURE = 'FeatureTime'
CONNECT_NAME = 'time-started'

_TIME_INSTANCE=None

def setup_feature(ss):
    if _TIME_INSTANCE == None:
        _TIME_INSTANCE=FeatureTime()

    return _TIME_INSTANCE

class FeatureTime(gobject.GObject):
    """Time plugin wrapper to exchange messages with py-dbus.

    :param uri: URI to the HTML file to be displayed.
    :type uri: str

    """

    __gproperties__ = {
         'time_state' : (
                   gobject.TYPE_STRING, # type
                   'State of feature Time', # nick name
                   'Returns whether feature is on/off', # description
                   'off', # default value
                   gobject.PARAM_READWRITE
                   ),
         'kw_match' : (
                    gobject.TYPE_BOOLEAN, # type
                    'Keyword Match', # nick name
                    'Boolean value for keyword', # description
                    False, # default value
                    gobject.PARAM_READWRITE
                    ),
         'svc_kw_match' : (
                    gobject.TYPE_BOOLEAN, # type
                    'Service Keyword Match', # nick name
                    'Boolean value for keyword', # description
                    False, # default value
                    gobject.PARAM_READWRITE
                    ),
         'now_time' : (
                        gobject.TYPE_STRING, # type
                        'Current Time', # nick name
                        'Value of current time', # description
                        None, # default value
                        gobject.PARAM_READWRITE
                      ),
         'now_date' : (
                        gobject.TYPE_STRING, # type
                        'Current Date', # nick name
                        'Value of current date', # description
                        None, # default value
                        gobject.PARAM_READWRITE
                      ),
         'espeak_msg' : (
                        gobject.TYPE_STRING, # type
                        'Espeak Message', # nick name
                        'String of message were sending to espeak', # description
                        None, # default value
                        gobject.PARAM_READWRITE
                      ),
         'unique_id' : (
                        gobject.TYPE_STRING, # type
                        'Unique ID', # nick name
                        'Value of obj unique id', # description
                        None, # default value
                        gobject.PARAM_READWRITE
                      ),
         'name' : (
                        gobject.TYPE_STRING, # type
                        'Obj Name', # nick name
                        'Name of Obj', # description
                        None, # default value
                        gobject.PARAM_READWRITE
                      ),
         'state' : (
                        gobject.TYPE_STRING, # type
                        'Objects state', # nick name
                        'State of object', # description
                        None, # default value
                        gobject.PARAM_READWRITE
                      ),
         'state_attributes' : (
                        gobject.TYPE_STRING, # type
                        'State attributes', # nick name
                        'Value of geature obj state attrs', # description
                        None, # default value
                        gobject.PARAM_READWRITE
                      )
    }

    __gsignals__ = {
    'time-started' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_STRING,)),
    'kw-match-set' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_STRING,)),
    'svc-kw-match-set' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_STRING,)),
    'service-say' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_STRING,))
    }

    capability = []

    def __init__(self, *args, **kwargs):
        # Initialize to be able to emit signals
        gobject.GObject.__init__(self)
        self.time_state = 'on' # device is on
        self.kw_match   = False # set to true when keyword identified
        self.svc_kw_match = False
        #super(FeatureTime, self).__init__(args, kwargs)
        self.name = "scarlett_time"
        self.now = self.set_now()
        self.now_time = self.get_current_time()
        self.now_date = self.get_current_date()
        scarlett.log.debug(
            Fore.YELLOW +
            "FeatureTime CREATED")
        self.state = None
        self.state_attributes = {}

    # GObject translates all the underscore characters to hyphen
    # characters so if you have a property called background_color,
    # its internal and valid name will be background-color.
    def do_get_property(self, property):
        if property.name == 'kw-match':
            return self.kw_match
        elif property.name == 'svc-kw-match':
            return self.svc_kw_match
        elif property.name == 'time-state':
            return self.time_state
        elif property.name == 'now-time':
            return self.now_time
        elif property.name == 'now-date':
            return self.now_date
        elif property.name == 'name':
            return self.name
        elif property.name == 'state':
            return self.state
        elif property.name == 'state-attribute':
            return self.state_attributes
        else:
            raise AttributeError, 'unknown property %s' % property.name

    def do_set_property(self, property, value):
         if property == 'kw-match':
             self.kw_match = value
         elif property == 'svc-kw-match':
             self.svc_kw_match = value
         elif property == 'time-state':
             self.time_state = value
         elif property == 'now-time':
             self.now_time = value
         elif property == 'now-date':
             self.now_date = value
         elif property == 'name':
             self.name = value
         elif property == 'state':
             self.state = value
         elif property == 'state-attributes':
             self.state_attributes = value
         else:
             raise AttributeError, 'unknown property %s' % property

    def time_play(self, cmd='time'):
        self.current_time = self.get_current_time()
        self.current_date = self.get_current_date()
        scarlett.log.debug(
            Fore.YELLOW +
            "self.current_time: " +
            self.current_time)
        scarlett.log.debug(
            Fore.YELLOW +
            "self.current_date: " +
            self.current_date)

        # emit scarlett_speak
        say_current_time = scarlett_event("scarlett_speak",
            data=self.get_property('now-time')
            )
        self.emit('service-say', say_current_time)

        # set brain back to normal

        ## TODO: 2/13/2015 # Move all speaking logic to the main thread
        ### TODO # scarlett_says.say_block(self.current_time)
        ### TODO # scarlett_says.say_block(self.current_date)

        ## TODO: 2/13/2015 # Move all brain logic to the main thread
        ### TODO # self.failed = int(self.brain.set_brain_item_r('scarlett_failed', 0))
        ### TODO # self.keyword_identified = int(
        ### TODO #     self.brain.set_brain_item_r(
        ### TODO #         'm_keyword_match',
        ### TODO #         0))

    def get_current_time(self):
        self.now = self.set_now()
        self.do_set_property('now-time', self.now.strftime("It is now, %I:%M %p"))
        return self.now_time

    def get_current_date(self):
        self.now = self.set_now()
        self.do_set_property('now-date', self.now.strftime("Today's date is, %A, %B %d, %Y"))
        return self.now_date

    def set_now(self, override=False):
        if override:
            self.now = override
            return override
        return datetime.datetime.now()

    def get_time(self):
        return self.now

    def do_time_started(self, now_time):
        scarlett.log.info(
            Fore.GREEN +
            "self.current_time: " +
            now_time)

    def start(self):
        # register service start
        register_sstart = scarlett_event("service_state",
            data=self.get_property('time-state')
            )
        self.emit('time-started', register_sstart)

# Register to be able to emit signals
gobject.type_register(FeatureTime)

