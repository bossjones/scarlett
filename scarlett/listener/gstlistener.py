import scarlett
from scarlett.commands import Command
from scarlett.listener import *


# this is very important, without this, callbacks from gstreamer thread
# will messed our program up
import gobject
gobject.threads_init()

# source: http://stackoverflow.com/questions/8005765/how-to-get-duration-of-steaming-data-with-gstreamer
# # LETS TRY USING THIS: # gobject.threads_init()

# EXAMPLES source code: http://cgit.freedesktop.org/gstreamer/gst-python/tree/examples/filesrc.py?h=0.10

# gst.STATE_PLAYING Used to start playing
#  * player_name.set_state(gst.STATE_PLAYING)
# gst.STATE_PAUSED Used to pause file
#  * player_name.set_state(gst.STATE_PAUSED)
# gst.STATE_NULL Used to stop file
#  * player_name.set_state(gst.STATE_NULL)

class GstListener(Listener):
    """
    Controls all actions involving pocketsphinx, stt, and tts.
    """

    def __init__(self, lis_type, voice, override_parse=False, *args, **kwargs):
        scarlett.log.debug(Fore.YELLOW + 'Starting up GstListener')
        self.successes = 0
        self.failed = 0
        self.keyword_identified = 0
        self.lis_type = lis_type
        self.voice = voice
        self.commander = Command(self.voice)
        self.config = scarlett.config
        self.override_parse = override_parse
        Listener.__init__(self, lis_type)

        # "/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k"
        self.ps_hmm = self.get_hmm_full_path()
        self.ps_dict = self.get_dict_full_path()
        self.ps_lm = self.get_lm_full_path()
        self.ps_device = self.config.get('audio','usb_input_device')

        self.speech_system = self.config.get('speech', 'system')

        # default, use what we have set
        self.parse_launch_array = self._get_pocketsphinx_definition(override_parse)

        scarlett.log.debug(Fore.YELLOW + 'Initializing gst-parse-launch -------->')
        self.pipeline = gst.parse_launch(
           ' ! '.join(self.parse_launch_array))

        listener = self.pipeline.get_by_name('listener')
        listener.connect('result', self.__result__)
        listener.set_property('configured', True)

        scarlett.log.debug(Fore.YELLOW + "Initializing connection to vader element -------->")
        # TODO: Play with vader object some more
        #vader = self.pipeline.get_by_name("vader")
        #vader.connect("vader-start", self._on_vader_start)
        #vader.connect("vader-stop", self._on_vader_stop)

        scarlett.log.debug(Fore.YELLOW + "Initializing Bus -------->")
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        scarlett.log.debug(Fore.YELLOW + "Sending Message to Bus ---------->")
        bus.connect('message::application', self.__application_message__)

        # TODO: TEST EOS AND RESETTING PIPLINE
        #scarlett.log.debug(Fore.YELLOW + "After Message to Bus ----------->")
        #bus.connect("message::eos", self._on_bus_message_eos)

        # Scarlett's greetings
        self.voice.greetings_play()
        scarlett.log.debug(Fore.YELLOW + "KEYWORDS WE'RE LOOKING FOR: " + self.config.get('scarlett', 'owner'))
        self.pipeline.set_state(gst.STATE_PLAYING)

    def scarlett_start_listen(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def scarlett_stop_listen(self):
        self.pipeline.set_state(gst.STATE_NULL)

    def scarlett_pause_listen(self):
        self.pipeline.set_state(gst.STATE_PAUSED)

    def scarlett_restart_listen(self):
        self.scarlett_stop_listen()
        self.scarlett_start_listen()

    def partial_result(self, asr, text, uttid):
        """Forward partial result signals on the bus to the main thread."""

    def result(self, hyp, uttid):
        """Forward result signals on the bus to the main thread."""
        scarlett.log.debug(Fore.YELLOW + "Inside result function")
        if hyp in self.config.get('scarlett', 'keywords'):
            scarlett.log.debug(Fore.YELLOW + "HYP-IS-SOMETHING: " + hyp + "\n\n\n")
            scarlett.log.debug(Fore.YELLOW + "UTTID-IS-SOMETHING:" + uttid + "\n")
            self.failed = 0
            self.keyword_identified = 1
            self.voice.play('pi-listening')
        else:
            self.failed += 1
            scarlett.log.debug(Fore.YELLOW + "self.failed = %i" % (self.failed))
            if self.failed > 4:
                # reset pipline
                self.pipeline.set_state(gst.STATE_NULL)
                self.voice.speak(
                    " %s , if you need me, just say my name." %
                    (self.config.get('scarlett','owner')))
                self.failed = 0
                # TODO: If this REALLY doesn't work, DISABLED IT
                self.keyword_identified = 0
                self.pipeline.set_state(gst.STATE_PLAYING)
                self.voice.play('cancel')

    def run_cmd(self, hyp, uttid):
        scarlett.log.debug(Fore.YELLOW + "Inside run_cmd function")
        scarlett.log.debug(Fore.YELLOW + "KEYWORD IDENTIFIED BABY")
        scarlett.log.debug(Fore.RED + "self.keyword_identified = %i" % (self.keyword_identified))
        if hyp == 'CANCEL':
            self.cancel_listening()
        else:
            self.commander.check_cmd(hyp)
            scarlett.log.debug(Fore.RED + "AFTER run_cmd, self.keyword_identified = %i" % (self.keyword_identified))

    def listen(self, valve, vader):
        scarlett.log.debug(Fore.YELLOW + "Inside listen function" )
        self.pipeline.set_state(gst.STATE_PAUSED)
        self.voice.play('pi-listening')
        valve.set_property('drop', False)
        valve.set_property('drop', True)

    #def cancel_listening(self, valve):
    def cancel_listening(self):
        scarlett.log.debug(Fore.YELLOW + "Inside cancel_listening function" )
        #valve.set_property('drop', False)
        self.failed = 0
        self.keyword_identified = 0
        scarlett.log.debug(Fore.YELLOW + "self.failed = %i" % (self.failed))
        scarlett.log.debug(Fore.RED + "self.keyword_identified = %i" % (self.keyword_identified))
        self.scarlett_restart_listen()
        self.voice.play('pi-cancel')

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
        scarlett.log.debug(Fore.YELLOW + "Inside get_pipeline" )
        return self.pipeline

    def get_voice(self):
        scarlett.log.debug(Fore.YELLOW + "Inside get_voice" )
        return self.voice

    def destroy_listener(self):
        gtk.main_quit()

    def get_pipeline_state(self):
        return self.pipeline.get_state()

    def _get_pocketsphinx_definition(self,override_parse):
        scarlett.log.debug(Fore.YELLOW + "Inside _get_pocketsphinx_definition" )
        """Return ``pocketsphinx`` definition for :func:`gst.parse_launch`."""
        # default, use what we have set
        if override_parse == False:
            return [
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
                      'fakesink dump=1']
                      # NOTE, I commented out the refrence to the tee
                      # #'fakesink dump=1 t.'
        else:
            return override_parse

    def _get_vader_definition(self):
        scarlett.log.debug(Fore.YELLOW + "Inside _get_vader_definition" )
        """Return ``vader`` definition for :func:`gst.parse_launch`."""
        # source: https://github.com/bossjones/eshayari/blob/master/eshayari/application.py
        # Convert noise level from spin button range [0,32768] to gstreamer
        # element's range [0,1]. Likewise, convert silence from spin button's
        # milliseconds to gstreamer element's nanoseconds.

        # MY DEFAULT VADER DEFINITON WAS: vader name=vader auto-threshold=true
        # vader name=vader auto-threshold=true
        noise = 256 / 32768
        silence = 300 * 1000000
        return ("vader "
                        + "name=vader "
                        + "auto-threshold=false "
                        + "threshold=%.9f " % noise
                        + "run-length=%d " % silence
                        )


    def _on_vader_start(self, vader, pos):
        scarlett.log.debug(Fore.YELLOW + "Inside _on_vader_start" )
        """Send start position as a message on the bus."""
        import gst
        struct = gst.Structure("start")
        pos = pos / 1000000000 # ns to s
        struct.set_value("start", pos)
        vader.post_message(gst.message_new_application(vader, struct))

    def _on_vader_stop(self, vader, pos):
        scarlett.log.debug(Fore.YELLOW + "Inside _on_vader_stop" )
        """Send stop position as a message on the bus."""
        import gst
        struct = gst.Structure("stop")
        pos = pos / 1000000000 # ns to s
        struct.set_value("stop", pos)

    ### def _on_bus_message_eos(self, bus, message):
    ###     """Flush remaining subtitles to page."""
    ###     if self._text is not None:
    ###         # Store previous text.
    ###         self._texts[-1] = self._text
    ###         self._text = None
    ###     if self._starts and self._stops[-1] is not None:
    ###         self._append_subtitle(-1)
    ###         self._stop_speech_recognition()

    def __result__(self, listener, text, uttid):
        scarlett.log.debug(Fore.YELLOW + "Inside __result__" )
        """We're inside __result__"""
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        listener.post_message(gst.message_new_application(listener, struct))

    def __partial_result__(self, listner, text, uttid):
        scarlett.log.debug(Fore.YELLOW + "Inside __partial_result__" )
        """We're inside __partial_result__"""
        struct = gst.Structure('partial_result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        listener.post_message(gst.message_new_application(listener, struct))

    def __run_cmd__(self, listener, text, uttid):
        scarlett.log.debug(Fore.YELLOW + "Inside __run_cmd__" )
        """We're inside __run_cmd__"""
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        listener.post_message(gst.message_new_application(listener, struct))

    def __application_message__(self, bus, msg):
        msgtype = msg.structure.get_name()
        scarlett.log.debug(Fore.YELLOW + "msgtype: " + msgtype)
        if msgtype == 'partial_result':
            self.partial_result(msg.structure['hyp'], msg.structure['uttid'])
        elif msgtype == 'result':
            if self.keyword_identified == 1:
                self.run_cmd(msg.structure['hyp'], msg.structure['uttid'])
            else:
                self.result(msg.structure['hyp'], msg.structure['uttid'])
        elif msgtype == 'run_cmd':
            self.run_cmd(msg.structure['hyp'], msg.structure['uttid'])
        elif msgtype == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
        elif msgtype == gst.MESSAGE_ERROR:
            self.pipeline.set_state(gst.STATE_NULL)
            (err, debug) = msgtype.parse_error()
            scarlett.log.debug(Fore.RED + "Error: %s" % err, debug)
