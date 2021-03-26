import sys
import traceback
from functools import wraps


def handle_exception_in_method(method):
    '''
    All qt function which are called by qt itself should have a
    handle_exception_in_method decorator so that we can see the exceptions
    properly (PySide will loose the exception if we don't).
    '''

    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception:
            if traceback is not None:
                traceback.print_exc()
            if sys is not None:
                sys.excepthook(*sys.exc_info())
        finally:
            args = None
            kwargs = None

    return wrapper