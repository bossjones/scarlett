import scarlett
from scarlett.commands import Command
from scarlett.listener import *

class GstListener(Listener):

    def __init__(self, lis_type, override_parse=False):
        scarlett.log.debug(Fore.YELLOW + 'Starting up GstListener')
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
        scarlett.log.debug(Fore.YELLOW + "KEYWORDS WE'RE LOOKING FOR: " + self.config.get('scarlett', 'owner'))

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
            scarlett.log.debug(Fore.YELLOW + "HYP-IS-SOMETHING: " + hyp + "\n\n\n")
            scarlett.log.debug(Fore.YELLOW + "UTTID-IS-SOMETHING:" + uttid + "\n")
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
        scarlett.log.debug(Fore.YELLOW + "KEYWORD IDENTIFIED BABY")
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
