#!/usr/bin/env python
"""
Scarlett Client Utils
"""
import errno
import select as select_lib
import time
import socket

from scarlett.constants import DEFAULT_SCARLETT_PORT


class Stopwatch(object):

    """Timer class that keeps track of time remaining"""

    def __init__(self, time_remaining):
        if time_remaining is not None:
            self.stop_time = time.time() + time_remaining
        else:
            self.stop_time = None

    def get_time_remaining(self):
        if self.stop_time is None:
            return None

        current_time = time.time()
        if not self.has_time_remaining(current_time):
            return 0.0

        time_remaining = self.stop_time - current_time
        return time_remaining

    def has_time_remaining(self, time_comparison=None):
        time_comparison = time_comparison or self.get_time_remaining()
        if self.stop_time is None:
            return True

        return bool(time_comparison < self.stop_time)


def disambiguate_server_parameter(hostport_tuple):
    """Takes either a tuple of (address, port) or a string of 'address:port' and disambiguates them for us"""
    if isinstance(hostport_tuple, tuple):
        scarlett_host, scarlett_port = hostport_tuple
    elif ':' in hostport_tuple:
        scarlett_host, scarlett_possible_port = hostport_tuple.split(':')
        scarlett_port = int(scarlett_possible_port)
    else:
        scarlett_host = hostport_tuple
        scarlett_port = DEFAULT_SCARLETT_PORT

    return scarlett_host, scarlett_port


def select(rlist, wlist, xlist, timeout=None):
    """Behave similar to select.select, except ignoring certain types of exceptions"""
    rd_list = []
    wr_list = []
    ex_list = []

    select_args = [rlist, wlist, xlist]
    if timeout is not None:
        select_args.append(timeout)

    try:
        rd_list, wr_list, ex_list = select_lib.select(*select_args)
    except select_lib.error as exc:
        # Ignore interrupted system call, reraise anything else
        if exc[0] != errno.EINTR:
            raise

    return rd_list, wr_list, ex_list


def unlist(given_list):
    """Convert the (possibly) single item list into a single item"""
    list_size = len(given_list)
    if list_size == 0:
        return None
    elif list_size == 1:
        return given_list[0]
    else:
        raise ValueError(list_size)

# Taken from: http://stackoverflow.com/a/11735897
def get_local_ip():
    """ Tries to determine the local IP address of the machine. """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Use Google Public DNS server to determine own IP
        sock.connect(('8.8.8.8', 80))
        ip_addr = sock.getsockname()[0]
        sock.close()

        return ip_addr

    except socket.error:
        return socket.gethostbyname(socket.gethostname())

### TODO: Try this at some point and make testable
### def gst_available():
###     """Return ``True`` if :mod:`gst` module is available."""
###     try:
###         print "Checking for Python Gstreamer Bindings.......\n "
###         import gst
###         print "Found...."
###         return True
###     except Exception:
###         print "Python Gstreamer bindings are not found !\n\n"
###         return False
###
### def pocketsphinx_available():
###     """Return ``True`` if `pocketsphinx` gstreamer plugin is available."""
###     try:
###         print "Checking for Gstreamer Pocketsphinx plugins......\n"
###         import gst
###         print "Found !!!"
###         return gst.plugin_load_by_name("pocketsphinx") is not None
###     except Exception:
###         print "Gstreamer Pocketsphinx plugins not found !!! \n\n\n"
###         return False
