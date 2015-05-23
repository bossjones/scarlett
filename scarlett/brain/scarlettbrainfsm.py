# -*- coding: UTF-8 -*-

# Imports
import scarlett
#import thread
import threading
import time
import redis
import logging

from transitions import Machine

SCARLETT_ROLE = 'brain'

BRAIN_NAME = 'fsm'
CORE_OBJECT = 'ScarlettBrainFSM'

_INSTANCE = None

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def setup_core(ss):

    logging.info("redis_host: {}".format(scarlett.config.get('redis', 'host')))
    logging.info("redis_port: {}".format(scarlett.config.get('redis', 'port')))
    logging.info("redis_db: {}".format(scarlett.config.getint('redis', 'db')))

    global _INSTANCE

    if _INSTANCE == None:
        _INSTANCE = ScarlettBrainFSM(host=scarlett.config.get('redis', 'host'),
          port=scarlett.config.get('redis', 'port'),
          db=scarlett.config.getint('redis', 'db')
        )

    return _INSTANCE

class ScarlettBrainFSM(redis.Redis):
  """
  Wrapper for Redis buffered commands that uses a pipeline internally
  for buffering messages. A thread is run that
  periodically flushes the buffer pipeline.
  """
  states = ['initalize', 'ready','running', 'is_checking_states', 'time_change', 'done_checking_states']

  def __init__(self, *args, **kwargs):
    """ Constructor

    :type host: string
    :param host: ip address or dns name of redis server

    :type port: int
    :param port: port that redis is running on

    :type db: int
    :param db: default redis db
    """
    super(ScarlettBrainFSM, self).__init__(*args, **kwargs)

    self.name = scarlett.brain.scarlettbrainfsm.SCARLETT_ROLE

    # Initalize the state machine
    self.machine = Machine(model=self, states=scarlett.brain.scarlettbrainfsm.ScarlettBrainFSM.states, initial='initalize')

    # startup transition
    self.machine.add_transition(trigger='startup', source='initalize', dest='ready')

    # checking_states transition
    self.machine.add_transition(trigger='checking_states', source='ready', dest='is_checking_states', conditions=['is_ready'])

    # array / dict of state machines connected to scarlett
    self._machines = {}

    # Check interval, in seconds
    self.interval = 1

    logging.debug('running with %s and %s', args, kwargs)

  def run(self):
      """ Method that runs forever """
      logging.debug('running with %s and %s', self.args, self.kwargs)
      while True:
          logging.debug('Starting')
          # Do something
          print('Doing something imporant in the background')
          time.sleep(self.interval)
          logging.debug('Exiting')

  def thread_runner(self):
    """ Call this function when we're ready to start this thread  """
    # function to run in background, self.run
    thread = threading.Thread(name=self.name,target=self.run, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution

  def hello(self):
    print 'hello hello hello!'

  def is_ready(self):
    """ Ensures that  """
    if self.state == 'ready':
      return True
    else:
      return False

