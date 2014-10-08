from scarlett.basics import Voice, config

class Listener(object):

  def __init__(self, lis_type, gobject, gst, config):

    _listener_types = ['gearman','gst']

    self.lis_type               = lis_type
    self.keyword_identified     = 0
    self.config                 = config
    self.voice                  = Voice()

  def __str__(self):
    return "You are using a %s type Listener" % (self.lis_type)

  def get_type(self):
    return self.lis_type
