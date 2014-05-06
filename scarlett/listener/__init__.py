class Listener(object):

  def __init__(self, type):
    self.type = type

  def __str__(self):
    return "You are using a %s type Listener" % (self.type)
