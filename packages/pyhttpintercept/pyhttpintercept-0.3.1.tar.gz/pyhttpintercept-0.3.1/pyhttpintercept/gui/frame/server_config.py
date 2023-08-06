# encoding: utf-8

import logging_helper
from uiutil.tk_names import EW, NORMAL, DISABLED
from uiutil import BaseLabelFrame, Button, Position
from ..window.scenarios import ScenariosConfigWindow
from ..window.scenario import AddEditScenarioWindow
from ..window.redirect_uris import RedirectURIConfigWindow

logging = logging_helper.setup_logging()


class ServerConfigFrame(BaseLabelFrame):

    BUTTON_WIDTH = 15

    def __init__(self,
                 title=u'WebServer:',
                 intercept_server=None,
                 *args,
                 **kwargs):

        self.intercept_server = intercept_server

        super(ServerConfigFrame, self).__init__(title=title,
                                                *args,
                                                **kwargs)

        Button(text=u'Redirect URIs',
               width=self.BUTTON_WIDTH,
               sticky=EW,
               command=self.launch_redirection_config,
               tooltip=u'Configure the URIs\n'
                       u'you want to redirect')

        # TODO: we should be able to configure without requiring a server instance!
        Button(text=u'Scenarios',
               width=self.BUTTON_WIDTH,
               sticky=EW,
               column=Position.NEXT,
               command=self.launch_scenarios_config,
               state=DISABLED if self.intercept_server is None else NORMAL,
               tooltip=u'Modify, add\n'
                       u'or remove\n'
                       u'scenarios')

        Button(text=u'Active Scenario',
               width=self.BUTTON_WIDTH,
               sticky=EW,
               column=Position.NEXT,
               command=self.launch_active_scenario_config,
               state=DISABLED if self.intercept_server is None else NORMAL,
               tooltip=u'Configure settings\n'
                       u'for the current\n'
                       u'active scenario')

        self.nice_grid()

    def launch_redirection_config(self):
        RedirectURIConfigWindow(fixed=True,
                                parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

    def launch_scenarios_config(self):
        window = ScenariosConfigWindow(fixed=True,
                                       intercept_server=self.intercept_server,
                                       parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

        try:
            self.intercept_server.reload_config()
        except AttributeError as e:
            logging.exception(e)

    def launch_active_scenario_config(self):

        window = AddEditScenarioWindow(edit=True,
                                       fixed=True,
                                       intercept_server=self.intercept_server,
                                       parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

        try:
            self.intercept_server.reload_config()
        except AttributeError as e:
            logging.exception(e)
