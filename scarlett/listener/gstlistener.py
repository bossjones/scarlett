import scarlett
from scarlett.basics.voice import Voice
from scarlett.commands import Command
from scarlett.listener import Listener

import os
import json
import tempfile
import subprocess
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

class GstListener(Listener):

    def __init__(self, lis_type, override_parse=False):
        scarlett.log.debug('Starting up GstListener')
        self.failed = 0
        self.keyword_identified = 0
        self.lis_type = lis_type
        self.voice = Voice()
        self.commander = Command()
        self.config = scarlett.config
        Listener.__init__(self, lis_type)

        # "/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k"
        self.ps_hmm = self.get_hmm_full_path()
        self.ps_dict = self.get_dict_full_path()
        self.ps_lm = self.get_lm_full_path()
        self.ps_device = self.config.get('audio','usb_input_device')

        self.speech_system = self.config.get('speech', 'system')

        # default, use what we have set
        if override_parse == False:
            parse_launch_array = [
                      'alsasrc device=' +
                      self.ps_device,
                      'queue silent=false leaky=2 max-size-buffers=0 max-size-time=0 max-size-bytes=0',
                      'audioconvert',
                      'audioresample',
                      'audio/x-raw-int, rate=16000, width=16, depth=16, channels=1',
                      'audioresample',
                      'audio/x-raw-int, rate=8000',
                      'vader name=vader auto-threshold=true',
                      'pocketsphinx lm=' +
                      self.ps_lm +
                      ' dict=' +
                      self.ps_dict +
                      ' hmm=' +
                      self.ps_hmm +
                      ' name=listener',
                      'fakesink dump=1 t.']
        else:
            parse_launch_array = override_parse


        self.pipeline = gst.parse_launch(
           ' ! '.join(parse_launch_array))

        listener = self.pipeline.get_by_name('listener')
        listener.connect('result', self.__result__)
        listener.set_property('configured', True)
        print "KEYWORDS WE'RE LOOKING FOR: " + self.config.get('scarlett', 'owner')

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
        if hyp in self.config.get('scarlett', 'keywords'):
            print "HYP-IS-SOMETHING: " + hyp + "\n\n\n"
            print "UTTID-IS-SOMETHING:" + uttid + "\n"
            self.failed = 0
            self.keyword_identified = 1
            self.voice.play('pi-listening')
        else:
            self.failed += 1
            if self.failed > 4:
                self.voice.speak(
                    " %s , if you need me, just say my name." %
                    (self.config('scarlett_owner')))
                self.failed = 0

    def run_cmd(self, hyp, uttid):
        print "KEYWORD IDENTIFIED BABY"
        self.check_cmd.commander(hyp)

    def listen(self, valve, vader):
        self.pipeline.set_state(gst.STATE_PAUSED)
        self.voice.play('pi-listening')
        valve.set_property('drop', False)
        valve.set_property('drop', True)

    def cancel_listening(self, valve):
        self.voice.play('pi-cancel')
        valve.set_property('drop', False)
        self.pipeline.set_state(gst.STATE_PLAYING)

# DISABLED 10/8/2014 #  # question - sound recording
# DISABLED 10/8/2014 #  def answer(self, question):
# DISABLED 10/8/2014 #    self.voice.play('pi-cancel')
# DISABLED 10/8/2014 #
# DISABLED 10/8/2014 #    print " * Contacting Google"
# DISABLED 10/8/2014 #    destf = tempfile.mktemp(suffix='piresult')
# DISABLED 10/8/2014 #    os.system('wget --post-file %s --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7" --header="Content-Type: audio/x-flac; rate=16000" -O %s -q "https://www.google.com/speech-api/v1/recognize?client=chromium&lang=en-US"' % (question, destf))
# DISABLED 10/8/2014 #    b = open(destf)
# DISABLED 10/8/2014 #    result = b.read()
# DISABLED 10/8/2014 #    b.close()
# DISABLED 10/8/2014 #
# DISABLED 10/8/2014 #    os.unlink(question)
# DISABLED 10/8/2014 #    os.unlink(destf)
# DISABLED 10/8/2014 #
# DISABLED 10/8/2014 #    if len(result) == 0:
# DISABLED 10/8/2014 #      print " * nop"
# DISABLED 10/8/2014 #      self.voice.play('pi-cancel')
# DISABLED 10/8/2014 #    else:
# DISABLED 10/8/2014 #      brain = Brain(json.loads(result))
# DISABLED 10/8/2014 #      if brain.think() == False:
# DISABLED 10/8/2014 #        print " * nop2"
# DISABLED 10/8/2014 #        self.voice.play('pi-cancel')
# DISABLED 10/8/2014 #
# DISABLED 10/8/2014 #    self.pipeline.set_state(gst.STATE_PLAYING)

    def get_hmm_full_path(self):
        if os.environ.get('SCARLETT_HMM'):
            _hmm_full_path = os.environ.get('SCARLETT_HMM')
        else:
            _hmm_full_path = self.config.get('pocketsphinx','hmm')

        return _hmm_full_path

    def get_lm_full_path(self):
        if os.environ.get('SCARLETT_LM'):
            _lm_full_path = os.environ.get('SCARLETT_LM')
        else:
            _lm_full_path = self.config.get('pocketsphinx','lm')

        return _lm_full_path

    def get_dict_full_path(self):
        if os.environ.get('SCARLETT_DICT'):
            _dict_full_path = os.environ.get('SCARLETT_DICT')
        else:
            _dict_full_path = self.config.get('pocketsphinx','dict')

        return _dict_full_path

    def get_pipeline(self):
        return self.pipeline

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
        msgtype = msg.structure.get_name()
        if msgtype == 'partial_result':
            self.partial_result(msg.structure['hyp'], msg.structure['uttid'])
        elif msgtype == 'result':
            if self.keyword_identified == 1:
                self.run_cmd(msg.structure['hyp'], msg.structure['uttid'])
            else:
                self.result(msg.structure['hyp'], msg.structure['uttid'])
        elif msgtype == 'run_cmd':
            self.run_cmd(msg.structure['hyp'], msg.structure['uttid'])
            # self.pipeline.set_state(gst.STATE_PAUSED)
