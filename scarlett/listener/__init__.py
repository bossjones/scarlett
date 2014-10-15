import scarlett
from scarlett.basics.voice import Voice
from scarlett.constants import *


class Listener(object):

    def __init__(self, lis_type):

        _listener_types = ['gearman', 'gst']

        self.lis_type = lis_type
        self.keyword_identified = 0
        self.config = scarlett.config
        # self.voice                  = Voice()

    def __str__(self):
        return "You are using a %s type Listener" % (self.lis_type)

    def get_type(self):
        return self.lis_type
