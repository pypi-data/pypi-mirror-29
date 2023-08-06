# encoding: utf-8

import logging_helper
from tkinter.constants import NSEW
from uiutil.window.child import ChildWindow
from ..frame.redirect_uris import RedirectURIConfigFrame

logging = logging_helper.setup_logging()


class RedirectURIConfigWindow(ChildWindow):

    def __init__(self,
                 *args,
                 **kwargs):

        super(RedirectURIConfigWindow, self).__init__(*args,
                                                      **kwargs)

    def _setup(self):
        self.title(u"Redirect URI Configuration")

        self.config = RedirectURIConfigFrame(parent=self._main_frame)
        self.config.grid(sticky=NSEW)
