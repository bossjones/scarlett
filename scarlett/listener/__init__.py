import scarlett

class Listener(object):

  def __init__(self, lis_type):
    self.lis_type               = lis_type
    self.keyword_identified = 0

  def __str__(self):
    return "You are using a %s type Listener" % (self.lis_type)

  def get_type(self):
    return self.lis_type
