# encoding: utf-8

import logging_helper
from tkinter.constants import NSEW
from uiutil.window.child import ChildWindow
from ..frame.scenario import AddEditScenarioFrame

logging = logging_helper.setup_logging()


BLUE_TEXT_RADIO_BUTTON = u"BlueText.TRadiobutton"
BLUE_TEXT_BUTTON = u"BlueText.TButton"
BLUE_TEXT_LABEL = u"BlueText.TLabel"


class AddEditScenarioWindow(ChildWindow):

    def __init__(self,
                 selected_record=None,
                 edit=False,
                 intercept_server=None,
                 *args,
                 **kwargs):

        self.selected_record = selected_record
        self.edit = edit
        self.intercept_server = intercept_server

        super(AddEditScenarioWindow, self).__init__(*args,
                                                    **kwargs)

    def _setup(self):
        self.title(u"Add/Edit Intercept Scenario")

        self.config = AddEditScenarioFrame(parent=self._main_frame,
                                           selected_scenario=self.selected_record,
                                           edit=self.edit,
                                           intercept_server=self.intercept_server)
        self.config.grid(sticky=NSEW)
