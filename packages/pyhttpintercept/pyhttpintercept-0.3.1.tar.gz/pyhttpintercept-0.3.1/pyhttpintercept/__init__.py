
# Get module version
from _metadata import __version__

__all__ = [
    '__version__',
    'ThreadedHTTPWebServer',
    'HTTPWebServer',
    'InterceptServer',
    'BaseInterceptHandler',
    'BodyInterceptHandler',
    'ServerRootWindow',
    'ServerChildWindow',
    'ServerConfigRootWindow',
    'ServerConfigChildWindow'
]

# Import key items from module
from .server import (HTTPWebServer,
                     ThreadedHTTPWebServer,
                     InterceptServer)

from .intercept.handlers import (BaseInterceptHandler,
                                 BodyInterceptHandler)

from .gui import (ServerRootWindow,
                  ServerChildWindow,
                  ServerConfigRootWindow,
                  ServerConfigChildWindow)

# Set default logging handler to avoid "No handler found" warnings.
from logging import NullHandler, getLogger
getLogger(__name__).addHandler(NullHandler())
