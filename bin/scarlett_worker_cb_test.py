#!/usr/bin/env python

#  scarlettcmd worker
from gearman import *
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP

gm_worker = gearman.GearmanWorker(['127.0.0.1:4730'])

def task_listener_scarlettcmd_inflight(gearman_worker, gearman_job):
  print 'reporting status'
  print "LETS RUN THIS SCARLETT COMMAND: " + gearman_job.data
  stt     = gearman_job.data
  keyword = stt[:8]
  if keyword == "SCARLETT":
    sock.sendto(stt, (UDP_IP, UDP_PORT))
    return stt
  else:
    sock.sendto(stt, (UDP_IP, UDP_PORT))
  
  # return scarlett_cmd_to_run
  return stt

# set_client_id is optional
gm_worker.set_client_id('scarlett_listener')
gm_worker.register_task('scarlettcmd', task_listener_scarlettcmd_inflight)

gm_worker.work()

