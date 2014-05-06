#!/usr/bin/env python

"""
Scarlett Brain
"""

import scarlett
from voice import Voice
import nltk

class Brain:
  def __init__(self, resp):
    self.resp  = resp.get('hypotheses', [])
    self.voice = Voice()

  def think(self):
    if len(self.resp) == 0:
      return False

    #scarlett_config=ScarlettConfig()
    q = self.resp[0]['utterance']
    if q in ['nothing', 'cancel', 'no'] or len(q) <= 1:
      print " * Ignoring", q
      self.voice.speak("Okay")

    print " * Thinking about '%s'" % q
    nq = nltk.pos_tag(nltk.word_tokenize(q))

    cells = [(cell.test(q, nq), cell) for cell in GreyCell.__subclasses__()]
    cells = sorted(cells, key=lambda cell: cell[0])
    score, cell = cells[-1]

    print " * Cell %s scored %.2f, activating it" % (cell.__name__, score)

    self.voice.play('pi-response')
    try:
      r = cell()
      return r.activate(q, nq)
    except Exception as e:
      print e
      self.voice.speak("Something has gone terribly wrong " + self.voice.gimmie('scarlett_owner') + "\! Please try again.")
      return False

class GreyCell(object):
  @staticmethod
  def test(query, ntlk_processed_query):
    pass

  def activate(self, query, ntlk_processed_query):
    pass
