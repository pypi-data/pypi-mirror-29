# encoding: utf-8

from uiutil.window.root import RootWindow
from uiutil.window.child import ChildWindow
from ..frame.server_config import ServerConfigFrame


class _ServerConfigWindow(object):

    def __init__(self,
                 *args,
                 **kwargs):
        super(_ServerConfigWindow, self).__init__(*args,
                                                  **kwargs)

    def _setup(self):
        self.title(u'WebServer Config')
        self.dynamic_frame = ServerConfigFrame(parent=self._main_frame)


class ServerConfigRootWindow(_ServerConfigWindow, RootWindow):

    def __init__(self,
                 *args,
                 **kwargs):
        super(ServerConfigRootWindow, self).__init__(*args,
                                                     **kwargs)


class ServerConfigChildWindow(_ServerConfigWindow, ChildWindow):

    def __init__(self,
                 *args,
                 **kwargs):
        super(ServerConfigChildWindow, self).__init__(*args,
                                                      **kwargs)
