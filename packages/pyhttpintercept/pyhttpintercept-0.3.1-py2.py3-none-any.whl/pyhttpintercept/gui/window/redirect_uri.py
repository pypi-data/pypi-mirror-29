# encoding: utf-8

import logging_helper
from tkinter.constants import NSEW
from uiutil.window.child import ChildWindow
from ..frame.redirect_uri import AddEditRedirectURIFrame

logging = logging_helper.setup_logging()


class AddEditRedirectURIWindow(ChildWindow):

    def __init__(self,
                 selected_record=None,
                 edit=False,
                 *args,
                 **kwargs):

        self.selected_record = selected_record
        self.edit = edit

        super(AddEditRedirectURIWindow, self).__init__(*args,
                                                       **kwargs)

    def _setup(self):
        self.title(u"Add/Edit Redirect URI")

        self.config = AddEditRedirectURIFrame(parent=self._main_frame,
                                              selected_record=self.selected_record,
                                              edit=self.edit)
        self.config.grid(sticky=NSEW)
