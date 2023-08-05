import pickle
import cloudpickle
from google.appengine.api import taskqueue
from google.appengine.ext import db
import functools
from im_util import logdebug, logwarning, logexception, dumper, get_dump

TASKUTILS_TASKROUTE = "/_ah/task"

def set_taskroute(value):
    global TASKUTILS_TASKROUTE
    TASKUTILS_TASKROUTE = value

def get_taskroute():
    global TASKUTILS_TASKROUTE
    return TASKUTILS_TASKROUTE


def get_enqueue_url(suffix):
    return "%s/%s" % (get_taskroute(), suffix)

# _DEFAULT_WEBAPP_URL = "/_ah/task/(.*)"
# _DEFAULT_ENQUEUE_URL = "/_ah/task/%s"

_TASKQUEUE_HEADERS = {"Content-Type": "application/octet-stream"}

class Error(Exception):
    """Base class for exceptions in this module."""

class PermanentTaskFailure(Error):
    """Indicates that a task failed, and will never succeed."""

class RetryTaskException(Error):
    """Indicates that task needs to be retried."""

class _TaskToRun(db.Model):
    """Datastore representation of a deferred task.
    
    This is used in cases when the deferred task is too big to be included as
    payload with the task queue entry.
    """
    data = db.BlobProperty(required=True) # up to 1 mb

def _run(data, headers):
    """Unpickles and executes a task.
    
    Args:
      data: A pickled tuple of (function, args, kwargs) to execute.
    Returns:
      The return value of the function invocation.
    """
    try:
        func, args, kwargs, passthroughargs = pickle.loads(data)
    except Exception, e:
        raise PermanentTaskFailure(e)
    else:
        if passthroughargs.get("_run_from_datastore"):
            _run_from_datastore(headers, args[0])
        else:
            if passthroughargs.get("includeheaders"):
                kwargs["headers"] = headers
            func(*args, **kwargs)

def _run_from_datastore(headers, key):
    """Retrieves a task from the datastore and executes it.
    
    Args:
      key: The datastore key of a _DeferredTaskEntity storing the task.
    Returns:
      The return value of the function invocation.
    """
    logwarning("running task from datastore")
    entity = _TaskToRun.get(key)
    if entity:
        try:
            _run(entity.data, headers)
        except PermanentTaskFailure:
            entity.delete()
            raise
        else:
            entity.delete()

def task(f=None, **taskkwargs):
    if not f:
        return functools.partial(task, **taskkwargs)
    
    taskkwargscopy = dict(taskkwargs)
    
    def GetAndDelete(name, default = None):
        retval = default
        if name in taskkwargscopy:
            retval = taskkwargscopy[name]
            del taskkwargscopy[name]
        return retval
    queue = GetAndDelete("queue", "default")
    transactional = GetAndDelete("transactional", False)
    parent = GetAndDelete("parent")
    includeheaders = GetAndDelete("includeheaders", False)
    logname = GetAndDelete("logname", "%s/%s" % (getattr(f, '__module__', 'none'), getattr(f, '__name__', 'none')))

    taskkwargscopy["headers"] = dict(_TASKQUEUE_HEADERS)

    url = get_enqueue_url(logname)# _DEFAULT_ENQUEUE_URL % logname
    
    taskkwargscopy["url"] = url.lower()
    
    logdebug(taskkwargscopy)

    passthroughargs = {
        "includeheaders": includeheaders
    }

    @functools.wraps(f)    
    def runtask(*args, **kwargs):
        pickled = cloudpickle.dumps((f, args, kwargs, passthroughargs))
        logdebug("task pickle length: %s" % len(pickled))
        if get_dump():
            logdebug("f:")
            dumper(f)
            logdebug("args:")
            dumper(args)
            logdebug("kwargs:")
            dumper(kwargs)
            logdebug("passthroughargs:")
            dumper(passthroughargs)
        try:
            task = taskqueue.Task(payload=pickled, **taskkwargscopy)
            return task.add(queue, transactional=transactional)
        except taskqueue.TaskTooLargeError:
            pickledf = cloudpickle.dumps(f)
            pickleda = cloudpickle.dumps(args)
            pickledk = cloudpickle.dumps(kwargs)
            pickledp = cloudpickle.dumps(passthroughargs)
            logexception("task too large, need to use datastore (%s, %s, %s, %s)" % (len(pickledf), len(pickleda), len(pickledk), len(pickledp)))
            if parent:
                key = _TaskToRun(data=pickled, parent=parent).put()
            else:
                key = _TaskToRun(data=pickled).put()
            rfspickled = cloudpickle.dumps((None, [key], {}, {"_run_from_datastore": True}))
            task = taskqueue.Task(payload=rfspickled, **taskkwargscopy)
            return task.add(queue, transactional=transactional)
    return runtask

def isFromTaskQueue(headers):
    """ Check if we are currently running from a task queue """
    # As stated in the doc (https://developers.google.com/appengine/docs/python/taskqueue/overview-push#Task_Request_Headers)
    # These headers are set internally by Google App Engine.
    # If your request handler finds any of these headers, it can trust that the request is a Task Queue request.
    # If any of the above headers are present in an external user request to your App, they are stripped.
    # The exception being requests from logged in administrators of the application, who are allowed to set the headers for testing purposes.
    return bool(headers.get('X-Appengine-TaskName'))

# Queue & task name are already set in the request log.
# We don't care about country and name-space.
_SKIP_HEADERS = {'x-appengine-country', 'x-appengine-queuename', 'x-appengine-taskname', 'x-appengine-current-namespace'}
    
def _launch_task(pickled, name, headers):
    try:
        # Add some task debug information.
#         dheaders = []
#         for key, value in headers.items():
#             k = key.lower()
#             if k.startswith("x-appengine-") and k not in _SKIP_HEADERS:
#                 dheaders.append("%s:%s" % (key, value))
#         logdebug(", ".join(dheaders))
        logdebug(", ".join(["%s:%s" % (key, value) for key, value in headers.items()]))
        
        if not isFromTaskQueue(headers):
            raise PermanentTaskFailure('Detected an attempted XSRF attack: we are not executing from a task queue.')

        logdebug('before run "%s"' % name)
        _run(pickled, headers)
        logdebug('after run "%s"' % name)
    except PermanentTaskFailure:
        logexception("Aborting task")
    except:
        logexception("failure")
        raise
    # else let exceptions escape and cause a retry

