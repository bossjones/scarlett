#!/usr/bin/env python

#  scarlettcmd worker
from gearman import *
import argparse

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.unique

parser = argparse.ArgumentParser("CLI tool to test sending scarlett commands to gearman")

parser.add_argument("-c","--cmd",
                      action="store",
                      help = "Run Scarlett command string")

args = parser.parse_args()

scarlett_cmd = args.cmd if args.cmd else "SCARLETT WHAT TIME IS IT"

gm_client = gearman.GearmanClient(['127.0.0.1:4730'])

# See gearman/job.py to see attributes on the GearmanJobRequest
submitted_job_request = gm_client.submit_job("scarlettcmd", scarlett_cmd, priority=gearman.PRIORITY_HIGH, background=True)

check_request_status(submitted_job_request)
