import scarlett
import time
import datetime
from scarlett.features import *
import scarlett.basics.voice
import scarlett.basics.say as scarlett_says

import gobject

import dbus
import dbus.service

class FeatureTime(gobject.GObject):
    """Time plugin wrapper to exchange messages with py-dbus.

    :param uri: URI to the HTML file to be displayed.
    :type uri: str

    """

    __gproperties__ = {
         'state' : (
                   gobject.TYPE_BOOLEAN, # type
                   'State of feature Time', # nick name
                   'Returns whether feature is on/off', # description
                   False, # default value
                   gobject.PARAM_READWRITE
                   ),
         'kw_match' : (
                    gobject.TYPE_BOOLEAN, # type
                    'Keyword Match', # nick name
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
                      )
    }

    __gsignals__ = { 'time-started' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_BOOLEAN,))
    }

    capability = []

    def __init__(self, voice, brain, *args, **kwargs):
        # Initialize to be able to emit signals
        gobject.GObject.__init__(self,args, kwargs)
        self.state = True # device is on
        self.kw_match = False # set to true when keyword identified
        #super(FeatureTime, self).__init__(args, kwargs)
        self._name = "time"
        self.voice = voice
        self.brain = brain
        self.now = self.set_now()
        self.now_time = self.get_current_time()
        self.now_date = self.get_current_date()

    # GObject translates all the underscore characters to hyphen
    # characters so if you have a property called background_color,
    # its internal and valid name will be background-color.
    def do_get_property(self, property):
        if property.name == 'kw-match':
            return self.kw_match
        elif property.name == 'state':
            return self.state
        elif property.name == 'now-time':
            return self.now_time
        elif property.name == 'now-date':
            return self.now_date
        else:
            raise AttributeError, 'unknown property %s' % property.name

    def do_set_property(self, property, value):
         if property.name == 'kw-match':
             self.kw_match = value
         elif property.name == 'state':
             self.state = value
         elif property.name == 'now-time':
             self.now_time = value
         elif property.name == 'now-date':
             self.now_date = value
         else:
             raise AttributeError, 'unknown property %s' % property.name

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

        scarlett_says.say_block(self.current_time)
        scarlett_says.say_block(self.current_date)
        self.failed = int(self.brain.set_brain_item_r('scarlett_failed', 0))
        self.keyword_identified = int(
            self.brain.set_brain_item_r(
                'm_keyword_match',
                0))

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
        self.emit('time-started', self.get_property('now-time'))

# Register to be able to emit signals
gobject.type_register(FeatureTime)

