# encoding: utf-8

import logging_helper
from uiutil.tk_names import StringVar, askquestion, W, NORMAL, EW, HORIZONTAL, NSEW, E, S
from uiutil import BaseFrame, nice_grid
from ...config.intercept import InterceptConfig
from ...config.intercept_scenarios import Scenarios
from ..window.scenario import AddEditScenarioWindow

logging = logging_helper.setup_logging()

BLUE_TEXT = dict(foreground=u"blue")
BLUE_TEXT_RADIO_BUTTON = u"BlueText.TRadiobutton"
BLUE_TEXT_BUTTON = u"BlueText.TButton"
BLUE_TEXT_LABEL = u"BlueText.TLabel"


class ScenariosConfigFrame(BaseFrame):

    STYLES = {BLUE_TEXT_RADIO_BUTTON: BLUE_TEXT,
              BLUE_TEXT_BUTTON:       BLUE_TEXT,
              BLUE_TEXT_LABEL:        BLUE_TEXT,
              }

    def __init__(self,
                 intercept_server=None,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self, *args, **kwargs)

        self.intercept_server = intercept_server

        self._cfg = InterceptConfig()
        self._scenarios = Scenarios()

        self.__selected_scenario = StringVar(self.parent)
        self.__active_scenario = StringVar(self.parent,
                                           value=self._cfg.selected_scenario)

        self.columnconfigure(self.column.start(), weight=1)

        self.SCENARIO_ROW = self.row.next()
        self.rowconfigure(self.SCENARIO_ROW, weight=1)
        self.BUTTON_ROW = self.row.next()

        self.__build_scenarios_frame()
        self.__build_button_frame()

    def __build_scenarios_frame(self):

        self.scenarios_frame = BaseFrame(self)
        self.scenarios_frame.grid(row=self.SCENARIO_ROW,
                                  column=self.column.current,
                                  sticky=NSEW)

        left_col = self.scenarios_frame.column.start()
        right_col = self.scenarios_frame.column.next()
        headers_row = self.scenarios_frame.row.next()

        self.scenarios_frame.label(text=u'Scenario',
                                   row=headers_row,
                                   column=left_col)

        self.scenarios_frame.label(text=u'Description',
                                   row=headers_row,
                                   column=right_col)

        self.scenarios_frame.separator(orient=HORIZONTAL,
                                       row=self.scenarios_frame.row.next(),
                                       column=left_col,
                                       columnspan=2,
                                       sticky=EW,
                                       padx=5,
                                       pady=5)

        for scenario in sorted(self._scenarios.get_items(), key=lambda s: s.name):

            scenario_row = self.scenarios_frame.row.next()

            if scenario.name == self.__active_scenario.get():
                self.__selected_scenario.set(scenario.name)
                label_style = BLUE_TEXT_LABEL
                radio_button_style = BLUE_TEXT_RADIO_BUTTON

            else:
                label_style = u'TLabel'
                radio_button_style = u'TRadiobutton'

            self.scenarios_frame.radiobutton(text=scenario.name,
                                             variable=self.__selected_scenario,
                                             value=scenario.name,
                                             style=radio_button_style,
                                             row=scenario_row,
                                             column=left_col,
                                             sticky=W)

            self.scenarios_frame.label(text=scenario.description,
                                       style=label_style,
                                       row=scenario_row,
                                       column=right_col,
                                       sticky=W)

        self.scenarios_frame.separator(orient=HORIZONTAL,
                                       row=self.scenarios_frame.row.next(),
                                       column=left_col,
                                       columnspan=2,
                                       sticky=EW,
                                       padx=5,
                                       pady=5)

        self.scenarios_frame.nice_grid()

    def __build_button_frame(self):

        button_width = 15

        self.button_frame = BaseFrame(self)
        self.button_frame.grid(row=self.BUTTON_ROW,
                               column=self.column.current,
                               sticky=(E, W, S))

        button_row = self.button_frame.row.start()

        left_col = self.button_frame.column.start()
        left_middle_col = self.button_frame.column.next()
        middle_col = self.button_frame.column.next()
        right_middle_col = self.button_frame.column.next()
        right_col = self.button_frame.column.next()

        self.__close_button = self.button_frame.button(state=NORMAL,
                                                       text=u'Close',
                                                       width=button_width,
                                                       command=self.parent.master.exit,
                                                       row=button_row,
                                                       column=left_col)

        self.__set_active_button = self.button_frame.button(state=NORMAL,
                                                            text=u'Set Active',
                                                            width=button_width,
                                                            command=self.__set_active,
                                                            style=BLUE_TEXT_BUTTON,
                                                            row=button_row,
                                                            column=left_middle_col,
                                                            tooltip=(u'Set selected\n'
                                                                     u'scenario as\n'
                                                                     u'active'))

        self.__delete_scenario_button = self.button_frame.button(state=NORMAL,
                                                                 text=u'Delete Scenario',
                                                                 width=button_width+1,
                                                                 command=self.__delete_scenario,
                                                                 row=button_row,
                                                                 column=middle_col,
                                                                 tooltip=(u'Delete\n'
                                                                          u'selected\n'
                                                                          u'scenario'))

        self.__add_scenario_button = self.button_frame.button(state=NORMAL,
                                                              text=u'Add Scenario',
                                                              width=button_width,
                                                              command=self.__add_scenario,
                                                              row=button_row,
                                                              column=right_middle_col,
                                                              tooltip=(u'Add scenario\n'
                                                                       u'to scenarios\n'
                                                                       u'list'))

        self.__edit_scenario_button = self.button_frame.button(state=NORMAL,
                                                               text=u'Edit Scenario',
                                                               width=button_width,
                                                               command=self.__edit_scenario,
                                                               row=button_row,
                                                               column=right_col,
                                                               tooltip=(u'Edit\n'
                                                                        u'selected\n'
                                                                        u'scenario'))

        nice_grid(self.button_frame)

    def __add_scenario(self):
        window = AddEditScenarioWindow(fixed=True,
                                       intercept_server=self.intercept_server,
                                       parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

        self.scenarios_frame.destroy()
        self.__build_scenarios_frame()

        self.parent.master.update_geometry()

    def __edit_scenario(self):
        window = AddEditScenarioWindow(selected_record=self.__selected_scenario.get(),
                                       edit=True,
                                       fixed=True,
                                       intercept_server=self.intercept_server,
                                       parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

        self.scenarios_frame.destroy()
        self.__build_scenarios_frame()

        self.parent.master.update_geometry()

    def __delete_scenario(self):
        result = askquestion(u"Delete Scenario",
                             u"Are you sure you want to delete {t}?".format(t=self.__selected_scenario.get()),
                             icon=u'warning',
                             parent=self)

        if result == u'yes':
            # Delete selected scenario
            self._scenarios.delete(key_attr=self.__selected_scenario.get())

            self.scenarios_frame.destroy()
            self.__build_scenarios_frame()

            self.parent.master.update_geometry()

    def __set_active(self):

        # Set new active scenario
        self._cfg.selected_scenario = self.__selected_scenario.get()
        self.__active_scenario.set(self._cfg.selected_scenario)

        self.scenarios_frame.destroy()
        self.__build_scenarios_frame()
