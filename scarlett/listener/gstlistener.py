import scarlett
from listener import Listener
#from commander import Commander
from brain import Brain
#from cells.time import TimeNow, DateNow
import os
import json
import tempfile
import subprocess
import forecastio
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst
from scarlett import Voice

class GstListener(Listener):

  def __init__(self, lis_type, gobject, gst):
    self.failed                 = 0
    self.keyword_identified     = 0
    self.lis_type               = lis_type
    Listener.__init__(self, lis_type)

    self.lat                = scarlett.config.get('forecastio','lat')
    self.lng                = scarlett.config.get('forecastio','lng')
    self.api_key            = scarlett.config.get('forecastio','api_key')
    self.hmm                = "/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k"
    self.voice              = Voice()

    ### REFACTOR # self.arduino = Commander( scarlett.config('ARDUINO_ENABLED') )

    self.speech_system      = scarlett.config.get('speech','system')

    self.pipeline = gst.parse_launch(' ! '.join(['alsasrc device=' + scarlett.config.get('audio','usb_input_device'),
                                                  'queue silent=false leaky=2 max-size-buffers=0 max-size-time=0 max-size-bytes=0',
                                                  'audioconvert',
                                                  'audioresample',
                                                  'audio/x-raw-int, rate=16000, width=16, depth=16, channels=1',
                                                  'audioresample',
                                                  'audio/x-raw-int, rate=8000',
                                                  'vader name=vader auto-threshold=true',
                                                  'pocketsphinx lm=' + scarlett.config.get('pocketsphinx','lm') + ' dict=' + scarlett.config.get('pocketsphinx','dict') + ' hmm=' + self.hmm + ' name=listener',
                                                  'fakesink dump=1 t.']))

    listener = self.pipeline.get_by_name('listener')
    listener.connect('result', self.__result__)
    listener.set_property('configured', True)
    print "KEYWORDS WE'RE LOOKING FOR: " + scarlett.config.get('scarlett','owner')

    bus = self.pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect('message::application', self.__application_message__)
    self.pipeline.set_state(gst.STATE_PLAYING)

    # Scarlett's greetings
    self.voice.greetings_play()

  def partial_result(self, asr, text, uttid):
    """Forward partial result signals on the bus to the main thread."""

  def result(self, hyp, uttid):
    """Forward result signals on the bus to the main thread."""
    if hyp in scarlett.config.get('scarlett','keywords'):
      print "HYP-IS-SOMETHING: " + hyp + "\n\n\n"
      print "UTTID-IS-SOMETHING:" + uttid + "\n"
      self.failed = 0
      self.keyword_identified = 1
      self.voice.play('pi-listening')
    else:
      self.failed += 1
      if self.failed > 4:
        self.voice.speak( " %s , if you need me, just say my name." % (scarlett.config('scarlett_owner') ))
        self.failed = 0

  def run_cmd(self, hyp, uttid):
    print "KEYWORD IDENTIFIED BABY"
    self.check_cmd(hyp)

  def listen(self, valve, vader):
    self.pipeline.set_state(gst.STATE_PAUSED)
    self.voice.play('pi-listening')
    valve.set_property('drop',False)
    valve.set_property('drop',True)

  def cancel_listening(self, valve):
    self.voice.play('pi-cancel')
    valve.set_property('drop',False)
    self.pipeline.set_state(gst.STATE_PLAYING)

  # question - sound recording
  def answer(self, question):
    self.voice.play('pi-cancel')

    print " * Contacting Google"
    destf = tempfile.mktemp(suffix='piresult')
    os.system('wget --post-file %s --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7" --header="Content-Type: audio/x-flac; rate=16000" -O %s -q "https://www.google.com/speech-api/v1/recognize?client=chromium&lang=en-US"' % (question, destf))
    b = open(destf)
    result = b.read()
    b.close()

    os.unlink(question)
    os.unlink(destf)

    if len(result) == 0:
      print " * nop"
      self.voice.play('pi-cancel')
    else:
      brain = Brain(json.loads(result))
      if brain.think() == False:
        print " * nop2"
        self.voice.play('pi-cancel')

    self.pipeline.set_state(gst.STATE_PLAYING)

  def get_pipeline(self):
    return self.pipeline

  def check_cmd(self, command=''):

    command_master_list_hex = {
      "frizzytv": {
        "up": "1,77E1D009,32",
        "down": "1,77E1B009,32",
        "left": "1,77E11009,32",
        "right": "1,77E1E009,32",
        "menu": "1,77E1BA09,32",
        "pause": "1,77E12009,32",
        "play": "1,77E17A09,32",
        "circle button": "1,77E1BA09,32" # this too 77E12009
      },
      "appletv": {
        "up": "1,77E1D030,32",
        "down": "1,77E1B030,32",
        "left": "1,77E11030,32",
        "right": "1,77E1E030,32",
        "menu": "1,77E14030,32",
        "pause": "1,77E17A30,32",
        "play": "1,77E17A30,32",
        "circle button": "1,77E1BA30,32" 
      },
      "toshiba": {
        "channel up": "1,2FDD827,32",
        "channel down": "1,2FDF807,32",
        "volume up": "1,2FD58A7,32",
        "volume down": "1,2FD7887,32",
        "mute": "1,2FD08F7,32",
        "recall": "1,2FD38C7,32",
        "input": "1,2FDF00F,32",
        "select up": "1,2FD41BE,32",
        "select down": "1,2FDC13E,32",
        "select left": "1,2FDB847,32",
        "select right": "1,2FD9867,32",
        "select enter": "1,2FD916E,32",
        "one": "1,2FD807F,32",
        "two": "1,2FD40BF,32",
        "three": "1,2FDC03F,32",
        "four": "1,2FD20DF,32",
        "five": "1,2FDA05F,32",
        "six": "1,2FD609F,32",
        "seven": "1,2FDE01F,32",
        "eight": "1,2FD10EF,32",
        "nine": "1,2FD906F,32",
        "zero": "1,2FD00FF,32",
        "power": "1,2FD48B7,32"
      }
    }

    self.command = command

    self.spotify_commands = {
      "SPOTIFY PLAY": "play music",
      "SPOTIFY PAUSE": "pause music",
      "SPOTIFY SKIP": "skip track",
      "SPOTIFY SKIP FORWARD": "track back",
      "SPOTIFY SKIP BACK": "track forward",
    }
 
    self.light_commands = {
      "TURN ON THE LIGHTS": "hue lights on",
      "TURN ON LIGHTS": "hue lights on",
      "LIGHTS ON": "hue lights on",
      "TURN OFF THE LIGHTS": "hue lights off",
      "TURN OFF LIGHTS": "hue lights off",
      "LIGHTS OFF": "hue lights off",
      "TURN LIGHTS RED": "hue lights all red",
      "LIGHTS RED": "hue lights all red",
      "CHANGE LIGHTS RED": "hue lights all red",
      "TURN LIGHTS GREEN": "hue lights all green",
      "LIGHTS GREEN": "hue lights all green",
      "CHANGE LIGHTS GREEN": "hue lights all green",
      "TURN LIGHTS WHITE": "hue lights all white",
      "LIGHTS WHITE": "hue lights all white",
      "CHANGE LIGHTS WHITE": "hue lights all white",
      "TURN LIGHTS BRIGHTER": "echo '{\"bri\": 240}' | hue lights 3 state",
      "LIGHTS BRIGHTER": "echo '{\"bri\": 240}' | hue lights 3 state",
      "TURN LIGHTS DARKER": "echo '{\"bri\": 100}' | hue lights 3 state",
      "LIGHTS DARKER": "echo '{\"bri\": 100}' | hue lights 3 state",
      "SEXY TIME": "hue lights colorloop",
    }

    self.time_commands = {
      "WHAT TIME IS IT": "what time is it",
      "TIME IS IT": "what time is it",
      "TIME IT IS": "what time is it"
    }

    self.tv_commands = {
      "CHANNEL UP": "channel up",
      "CHANNEL DOWN": "channel down",
      "TURN TO MTV": "turn to mtv",
      "TURN TO BET": "turn to bet",
      "TURN TO HBO": "turn to hbo",
      "SWITCH TO APPLE TV": "switch to apple tv",
      "SWITCH TO PLAY STATION": "switch to play station",
      "SWTICH TO REGULAR TV": "switch to regular tv",
      "APPLE TV UP": command_master_list_hex["appletv"]["up"].lower(),
      "APPLE TV CHANNEL UP": command_master_list_hex["appletv"]["up"].lower(),
      "APPLE TV DOWN": command_master_list_hex["appletv"]["down"].lower(),
      "APPLE TV CHANNEL DOWN": command_master_list_hex["appletv"]["down"].lower(),
      "APPLE TV LEFT": command_master_list_hex["appletv"]["left"].lower(),
      "APPLE TV CHANNEL LEFT": command_master_list_hex["appletv"]["left"].lower(),
      "APPLE TV RIGHT": command_master_list_hex["appletv"]["right"].lower(),
      "APPLE TV CHANNEL RIGHT": command_master_list_hex["appletv"]["right"].lower(),
      "APPLE TV PAUSE": command_master_list_hex["appletv"]["pause"].lower(),
      "APPLE TV PLAY": command_master_list_hex["appletv"]["play"].lower(),
      "APPLE TV MENU": command_master_list_hex["appletv"]["menu"].lower(),
      "APPLE TV MENU BUTTON": command_master_list_hex["appletv"]["menu"].lower(),
      "APPLE TV ENTER": command_master_list_hex["appletv"]["circle button"].lower(),
      "APPLE TV ENTER BUTTON": command_master_list_hex["appletv"]["circle button"].lower()
    }

    self.general_commands = {
      "CANCEL": "cancel",
    }

    self.forecast_commands = {
      "WHAT IS THE FORECAST": "weather",
      "WHAT IS THE TEMPATURE": "weather",
      "WHAT IS CURRENT TEMPATURE": "weather",
      "WHATS THE WEATHER": "weather",
      "WHATS TODAYS WEATHER": "weather",
      "WHATS THE TEMPATURE": "weather",
    }

    if self.command in self.spotify_commands.keys():
        print "** received %s, sending 'spotify %s'" % (self.command, self.spotify_commands[self.command])
        self.spotify_play(self.spotify_commands[command])
    elif self.command in self.light_commands.keys():
        print "** received %s, sending 'light %s'" % (self.command, self.light_commands[self.command])
        try:
            print "trying light chit"
            self.light_play(self.light_commands[command])
        except Exception, e:
            print "light exception b. \nCMD: %s \nException: %s" % (command, e)
            self.general_play("cancel")
    elif self.command in self.time_commands.keys():
        print "** received %s, sending 'time %s'" % (self.command, self.time_commands[self.command])
        try:
            self.time_play(self.time_commands[command])
        except Exception, e:
            print "time exception b. \nCMD: %s \nException: %s" % (command, e)
            self.general_play("cancel")
    elif self.command in self.general_commands.keys():
      print "** received %s, sending 'general command: %s'" % (self.command, self.general_commands[self.command])
      self.general_play(self.general_commands[command])
    elif self.command in self.forecast_commands.keys():
      print "** received %s, sending 'forecast command: %s'" % (self.command, self.forecast_commands[self.command])
      self.forecast_play(self.forecast_commands[command])
    elif self.command in self.tv_commands.keys():
      print "** received %s, sending 'tv command: %s'" % (self.command, self.tv_commands[self.command])
      self.tv_play(self.tv_commands[command])

  def spotify_play(self,cmd):
    self.keyword_identified = 0
    self.voice.play('pi-response')
  def light_play(self,cmd):
    subprocess.call([cmd],shell=True)
    self.keyword_identified = 0
    self.voice.play('pi-response')
  def time_play(self,cmd):
    #### REFACTOR pi_time = pi.TimeNow().activate(self,"dont matter","dont matter")
    self.voice.speak("YOU KNOW WHAT TIME IT IS RIGHT NOW HOME BOY")
    self.keyword_identified = 0
    self.voice.play('pi-response')
  def general_play(self,cmd):
    self.keyword_identified = 0
    self.voice.play('pi-cancel')
  def tv_play(self,cmd):
    self.keyword_identified = 0
    self.voice.play('pi-response')
    #### REFACTOR # self.arduino.write(cmd)
    self.time.sleep(2)
  def forecast_play(self,cmd):
    self.keyword_identified = 0
    self.voice.play('pi-response')
    forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng)

    print forecast.hourly().data[0].temperature
    fio_hourly =  "%s degrees fahrenheit" % (forecast.hourly().data[0].temperature)
    fio_hourly = fio_hourly.replace(";","\;")
    self.voice.speak(fio_hourly)

    print "===========Hourly Data========="
    by_hour = forecast.hourly()
    print "Hourly Summary: %s" % (by_hour.summary)
    fio_summary = "Hourly Summary: %s" % (by_hour.summary)
    fio_summary = fio_summary.replace(";","\;")
    self.voice.speak(fio_summary)

    print "===========Daily Data========="
    by_day = forecast.daily()
    print "Daily Summary: %s" % (by_day.summary)
    fio_day = "Daily Summary: %s" % (by_day.summary)
    self.voice.speak(fio_day)

  def __result__(self, listener, text, uttid):
    """We're inside __result__"""
    struct = gst.Structure('result')
    struct.set_value('hyp', text)
    struct.set_value('uttid', uttid)
    listener.post_message(gst.message_new_application(listener, struct))
  def __partial_result__(self, listner, text, uttid):
    """We're inside __partial_result__"""
    struct = gst.Structure('partial_result')
    struct.set_value('hyp', text)
    struct.set_value('uttid', uttid)
    listener.post_message(gst.message_new_application(listener, struct))
  def __run_cmd__(self, listener, text, uttid):
   """We're inside __run_cmd__"""
   struct = gst.Structure('result')
   struct.set_value('hyp', text)
   struct.set_value('uttid', uttid)
   listener.post_message(gst.message_new_application(listener, struct))
  def __application_message__(self, bus, msg):
    msgtype =  msg.structure.get_name()
    if msgtype == 'partial_result':
      self.partial_result(msg.structure['hyp'], msg.structure['uttid'])
    elif msgtype == 'result':
      if self.keyword_identified ==  1:
        self.run_cmd(msg.structure['hyp'], msg.structure['uttid'])
      else:
        self.result(msg.structure['hyp'], msg.structure['uttid'])
    elif msgtype == 'run_cmd':
      self.run_cmd(msg.structure['hyp'], msg.structure['uttid'])
      #self.pipeline.set_state(gst.STATE_PAUSED)

