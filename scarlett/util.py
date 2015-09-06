"""
Scarlett Client Utils
"""

import socket

import Queue
import threading

from datetime import datetime
import re
import logging

MIN_WORKER_THREAD = 2

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) [%(module)s] %(message)s',)

DATE_STR_FORMAT = "%H:%M:%S %d-%m-%Y"

RE_SANITIZE_FILENAME = re.compile(r'(~|\.\.|/|\\)')
RE_SANITIZE_PATH = re.compile(r'(~|\.(\.)+)')
RE_SLUGIFY = re.compile(r'[^A-Za-z0-9_]+')


def sanitize_filename(filename):
    """ Sanitizes a filename by removing .. / and \\. """
    return RE_SANITIZE_FILENAME.sub("", filename)


def sanitize_path(path):
    """ Sanitizes a path by removing ~ and .. """
    return RE_SANITIZE_PATH.sub("", path)


def slugify(text):
    """ Slugifies a given text. """
    text = text.replace(" ", "_")

    return RE_SLUGIFY.sub("", text)


def datetime_to_str(dattim):
    """ Converts datetime to a string format.

    @rtype : str
    """
    return dattim.strftime(DATE_STR_FORMAT)

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


class ThreadPool(object):

    """ A priority queue-based thread pool. """
    # source: https://github.com/balloob/home-assistant/blob/master/homeassistant/util.py
    # pylint: disable=too-many-instance-attributes

    def __init__(self, job_handler, worker_count=0, busy_callback=None):
        """
        job_handler: method to be called from worker thread to handle job
        worker_count: number of threads to run that handle jobs
        busy_callback: method to be called when queue gets too big.
                       Parameters: worker_count, list of current_jobs,
                                   pending_jobs_count
        """
        self._job_handler = job_handler
        self._busy_callback = busy_callback

        self.worker_count = 0
        self.busy_warning_limit = 0
        self._work_queue = Queue.PriorityQueue()
        self.current_jobs = []
        self._lock = threading.RLock()
        self._quit_task = object()

        self.running = True

        for _ in range(worker_count):
            self.add_worker()

    def add_worker(self):
        """ Adds a worker to the thread pool. Resets warning limit. """
        with self._lock:
            if not self.running:
                raise RuntimeError("ThreadPool not running")

            worker = threading.Thread(target=self._worker)
            worker.daemon = True
            worker.start()

            self.worker_count += 1
            self.busy_warning_limit = self.worker_count * 3

    def remove_worker(self):
        """ Removes a worker from the thread pool. Resets warning limit. """
        with self._lock:
            if not self.running:
                raise RuntimeError("ThreadPool not running")

            self._work_queue.put(PriorityQueueItem(0, self._quit_task))

            self.worker_count -= 1
            self.busy_warning_limit = self.worker_count * 3

    def add_job(self, priority, job):
        """ Add a job to the queue. """
        with self._lock:
            if not self.running:
                raise RuntimeError("ThreadPool not running")

            self._work_queue.put(PriorityQueueItem(priority, job))

            # check if our queue is getting too big
            if self._work_queue.qsize() > self.busy_warning_limit \
               and self._busy_callback is not None:

                # Increase limit we will issue next warning
                self.busy_warning_limit *= 2

                self._busy_callback(
                    self.worker_count, self.current_jobs,
                    self._work_queue.qsize())

    def block_till_done(self):
        """ Blocks till all work is done. """
        self._work_queue.join()

    def stop(self):
        """ Stops all the threads. """
        with self._lock:
            if not self.running:
                return

            # Ensure all current jobs finish
            self.block_till_done()

            # Tell the workers to quit
            for _ in range(self.worker_count):
                self.remove_worker()

            self.running = False

            # Wait till all workers have quit
            self.block_till_done()

    def _worker(self):
        """ Handles jobs for the thread pool. """
        while True:
            # Get new item from work_queue
            # NOTE: Queue.get([block[, timeout]])
            # NOTE: Remove and return an item from the queue. If optional
            # NOTE: args block is true and timeout is None (the default),
            # NOTE: block if necessary until an item is available.
            # NOTE: If timeout is a positive number, it blocks at most
            # NOTE: timeout seconds and raises the Empty exception if no item
            # NOTE: was available within that time. Otherwise
            # NOTE: (block is false), return an item if one is immediately
            # NOTE: available, else raise the Empty exception
            # NOTE: (timeout is ignored in that case).
            job = self._work_queue.get().item

            if job == self._quit_task:
                self._work_queue.task_done()
                return

            # Add to current running jobs
            job_log = (datetime.now(), job)
            self.current_jobs.append(job_log)

            # Do the job
            self._job_handler(job)

            # Remove from current running job
            self.current_jobs.remove(job_log)

            # Tell work_queue the task is done
            self._work_queue.task_done()


class PriorityQueueItem(object):

    """ Holds a priority and a value. Used within PriorityQueue. """

    # pylint: disable=too-few-public-methods

    def __init__(self, priority, item):
        self.priority = priority
        self.item = item

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)
