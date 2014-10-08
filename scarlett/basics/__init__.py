import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst
from scarlett import *

class ScarlettBasics(object):

    def __init__(self):
      self.config = config
