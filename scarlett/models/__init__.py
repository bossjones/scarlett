import scarlett
from scarlett.constants import *
from stdnet import getdb,odm

class ScarlettModel(object):
    """ Class to route Event communication to all parts of scarlett """

    def __init__(self):
      self.config       = scarlett.config
      self.redis_host   = self.scarlett.config.get('redis','host')
      self.redis_port   = self.scarlett.config.get('redis','port')
      self.redis_db     = self.scarlett.config.get('redis','db')
      self.redis_server = getdb("redis://%s:%i?timeout=%i" % (self.redis_host,self.redis_port,self.redis_db) )
      self.pubsub       = None

    def get_redis_server(self):
      return self.redis_server

class FeatureItem(odm.StdModel):
    name=odm.SymbolField(unique=True)
    feature_keyword_identified = odm.FloatField()
    #size = odm.FloatField()
    dt = odm.DateField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = '-dt'


class ListenerItem(odm.StdModel):
    name=odm.SymbolField(unique=True)
    keyword_identified = odm.FloatField()
    dt = odm.DateField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = '-dt'
