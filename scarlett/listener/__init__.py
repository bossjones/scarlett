import scarlett
from scarlett.basics.voice import *
from scarlett.constants import *


class Listener(object):

    def __init__(self, lis_type, **kwargs):

        _listener_types = ['gearman', 'gst']

        self.lis_type = lis_type
        #self.brain = brain
        self.config = scarlett.config
        #self.voice  = voice

    def __str__(self):
        return "You are using a %s type Listener" % (self.lis_type)

    def get_type(self):
        return self.lis_type
