class ScarlettEventHook(object):
    """
    Simple event class used to provide hooks for different types of events in Scarlett.

    Here's how to use the ScarlettEventHook class::

        my_event = ScarlettEventHook()
        def on_my_event(a, b, **kw):
            print "Event was fired with arguments: %s, %s" % (a, b)
        my_event += on_my_event
        my_event.fire(a="foo", b="bar")
    """

    def __init__(self):
        self._handlers = []

    def __iadd__(self, handler):
        self._handlers.append(handler)
        return self

    def __isub__(self, handler):
        self._handlers.remove(handler)
        return self

    def fire(self, **kwargs):
        for handler in self._handlers:
            handler(**kwargs)

request_success = ScarlettEventHook()
"""
*request_success* is fired when a request is completed successfully.

Listeners should take the following arguments:

* *request_type*: Request type method used
* *name*: Path to the URL that was called (or override name if it was used in the call to the client)
* *response_time*: Response time in milliseconds
* *response_length*: Content-length of the response
"""

request_failure = ScarlettEventHook()
"""
*request_failure* is fired when a request fails

Event is fired with the following arguments:

* *request_type*: Request type method used
* *name*: Path to the URL that was called (or override name if it was used in the call to the client)
* *response_time*: Time in milliseconds until exception was thrown
* *exception*: Exception instance that was thrown
"""

scarlett_error = ScarlettEventHook()
"""
*scarlett_error* is fired when an exception occurs inside the execution of a Scarlett class.

Event is fired with the following arguments:

* *scarlett_instance*: Scarlett class instance where the exception occurred
* *exception*: Exception that was thrown
* *tb*: Traceback object (from sys.exc_info()[2])
"""

report_to_master = ScarlettEventHook()
"""
*report_to_master* is used when Scarlett is running in --slave mode. It can be used to attach
data to the dicts that are regularly sent to the master. It's fired regularly when a report
is to be sent to the master server.

Note that the keys "stats" and "errors" are used by Scarlett and shouldn't be overridden.

Event is fired with the following arguments:

* *client_id*: The client id of the running scarlett process.
* *data*: Data dict that can be modified in order to attach data that should be sent to the master.
"""

slave_report = ScarlettEventHook()
"""
*slave_report* is used when Scarlett is running in --master mode and is fired when the master
server receives a report from a Scarlett slave server.

This event can be used to aggregate data from the scarlett slave servers.

Event is fired with following arguments:

* *client_id*: Client id of the reporting scarlett slave
* *data*: Data dict with the data from the slave node
"""

hatch_complete = ScarlettEventHook()
"""
*hatch_complete* is fired when all scarlett users has been spawned.

Event is fire with the following arguments:

* *user_count*: Number of users that was hatched
"""

quitting = ScarlettEventHook()
"""
*quitting* is fired when the scarlett process in exiting
"""

master_start_hatching = ScarlettEventHook()
"""
*master_start_hatching* is fired when we initiate the hatching process on the master.

This event is especially usefull to detect when the 'start' button is clicked on the web ui.
"""

master_stop_hatching = ScarlettEventHook()
"""
*master_stop_hatching* is fired when terminate the hatching process on the master.

This event is especially usefull to detect when the 'stop' button is clicked on the web ui.
"""

scarlett_start_hatching = ScarlettEventHook()
"""
*scarlett_start_hatching* is fired when we initiate the hatching process on any scarlett worker.
"""

scarlett_stop_hatching = ScarlettEventHook()
"""
*scarlett_stop_hatching* is fired when terminate the hatching process on any scarlett worker.
"""
