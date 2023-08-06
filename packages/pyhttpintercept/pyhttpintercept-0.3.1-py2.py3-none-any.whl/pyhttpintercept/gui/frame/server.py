# encoding: utf-8

import logging_helper
from tkinter.messagebox import showerror
from uiutil import Position
from uiutil.tk_names import NORMAL, HORIZONTAL, W, EW
from pydnserver.gui.frame.dns_config_launcher import DNSConfigLauncherFrame
from networkutil.gui.endpoint_config_launcher_frame import EndpointsLauncherFrame, ROOT_LAYOUT
from uiutil.frame.frame import BaseFrame
from uiutil.widget.label import Label
from uiutil.widget.button import Button
from uiutil.widget.switchbox import SwitchBox, Switch
from classutils.decorators import profiling
from pyhttpintercept.server.server import InterceptServer
from ..frame.server_config import ServerConfigFrame
from ..._constants import (PROFILER_PROFILE_ID,
                           PROFILE,
                           THREADED,
                           START_SERVERS,
                           STOP_SERVERS)

logging = logging_helper.setup_logging()


class ServerFrame(BaseFrame):

    BUTTON_WIDTH = 20

    def __init__(self,
                 server=InterceptServer,
                 server_kwargs=None,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self,
                           *args,
                           **kwargs)

        if server_kwargs is None:
            server_kwargs = {}

        self.intercept_server = server(**server_kwargs)

        Label(text=u'Endpoints:',
              sticky=W)

        self.endpoints_config = EndpointsLauncherFrame(layout_key=ROOT_LAYOUT,
                                                       row=Position.NEXT,
                                                       column=Position.START,
                                                       sticky=EW,
                                                       columnspan=2)

        self.separator(orient=HORIZONTAL,
                       row=Position.NEXT,
                       columnspan=2,
                       sticky=EW,
                       padx=5,
                       pady=5)

        self.dns_config = DNSConfigLauncherFrame(row=Position.NEXT,
                                                 sticky=EW)

        self.intercept_config = ServerConfigFrame(intercept_server=self.intercept_server,
                                                  column=Position.NEXT,
                                                  sticky=EW)

        self.horizontal_separator(columnspan=2)

        self.switches = SwitchBox(text=THREADED,
                                  row=Position.NEXT,
                                  column=Position.START,
                                  sticky=W,
                                  sort=False,
                                  switches=(THREADED,
                                            PROFILE),
                                  switch_states={THREADED: Switch.ON,
                                                 PROFILE: Switch.OFF},
                                  switch_parameters={THREADED: {u"tooltip": u"Check to Run intercept\n"
                                                                            u"with threading enabled"},
                                                     PROFILE:  {u"tooltip": u"When profiling is enabled,\n"
                                                                            u"the logs will contain\n"
                                                                            u"information to help\n"
                                                                            u"identify bottlenecks in\n"
                                                                            u"handlers and modifiers.\n\n"
                                                                            u"Note: Only effective when\n"
                                                                            u"profiling is enabled from\n"
                                                                            u"debug menu!",
                                                                u'trace': self._update_profile}})

        self.start_stop_button = Button(state=NORMAL,
                                        value=START_SERVERS,
                                        width=self.BUTTON_WIDTH,
                                        command=self.start_stop,
                                        column=Position.NEXT,
                                        sticky=EW,
                                        tooltip=u'')

    def start_stop(self):
        if self.start_stop_button.value == START_SERVERS:
            self.start()
        else:
            self.stop()

    def start(self):

        try:
            self.intercept_server.start(threaded=self.switches.switch_state(THREADED))
            self.start_stop_button.value = STOP_SERVERS
            self.switches.switches[THREADED].disable()
            self.start_stop_button.tooltip.text = (u'Stop the\n'
                                                   u'running\n'
                                                   u'Intercept\n'
                                                   u'Servers.')

        except Exception as err:
            logging.exception(err)
            logging.fatal(u'Unexpected Exception.')

            showerror(title=u'Server startup failed!',
                      message=u'Failed to start intercept servers: {err}'.format(err=err))

            self.stop()

    def stop(self):

        self.intercept_server.stop()
        self.start_stop_button.value = START_SERVERS
        self.switches.switches[THREADED].enable()
        self.start_stop_button.tooltip.text = (u'Start Intercept\n'
                                               u'Servers for\n'
                                               u'active devices')

    def _update_profile(self):
        if self.switches.switch_state(PROFILE):
            profiling.enable(profile_id=PROFILER_PROFILE_ID)

        else:
            profiling.disable(profile_id=PROFILER_PROFILE_ID)
