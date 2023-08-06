# encoding: utf-8

import logging_helper
from tkinter.constants import NSEW
from uiutil.window.child import ChildWindow
from ..frame.scenarios import ScenariosConfigFrame

logging = logging_helper.setup_logging()


BLUE_TEXT_RADIO_BUTTON = u"BlueText.TRadiobutton"
BLUE_TEXT_BUTTON = u"BlueText.TButton"
BLUE_TEXT_LABEL = u"BlueText.TLabel"


class ScenariosConfigWindow(ChildWindow):

    def __init__(self,
                 intercept_server=None,
                 *args, **kwargs):

        self.intercept_server = intercept_server

        super(ScenariosConfigWindow, self).__init__(*args,
                                                    **kwargs)

    def _setup(self):
        self.title(u"Intercept Scenarios Config")

        self.config = ScenariosConfigFrame(parent=self._main_frame,
                                           intercept_server=self.intercept_server)
        self.config.grid(sticky=NSEW)
