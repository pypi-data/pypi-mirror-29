# encoding: utf-8

import logging_helper
from tkinter import IntVar, StringVar, BooleanVar
from tkinter.constants import W, DISABLED, NORMAL, EW, HORIZONTAL, NSEW
from fdutil.list_tools import filter_list
from uiutil.frame.frame import BaseFrame
from uiutil.helper.layout import nice_grid
from networkutil.gui.pickler_frame import RequestPicklerWindow
from ...config.constants import ModifierConstant, ScenarioConstant
from ...config.intercept import InterceptConfig
from ...config.intercept_handlers import Handlers
from ...config.intercept_scenarios import Scenarios
from ...intercept import InterceptModifiers
from ...intercept.handlers.support import make_modifier_tooltip_from_docstring

logging = logging_helper.setup_logging()


BLUE_TEXT_RADIO_BUTTON = u"BlueText.TRadiobutton"
BLUE_TEXT_BUTTON = u"BlueText.TButton"
BLUE_TEXT_LABEL = u"BlueText.TLabel"


class AddEditScenarioFrame(BaseFrame):

    def __init__(self,
                 selected_scenario=None,
                 edit=False,
                 intercept_server=None,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self, *args, **kwargs)

        self._cfg = InterceptConfig()
        self._scenarios = Scenarios()
        self._handlers = Handlers()
        self._modifiers = InterceptModifiers()
        self._modifiers.load_all_modifiers()  # Do we really need to do this? (Docstrings currently require this)

        self.intercept_server = intercept_server
        self.edit = edit
        self.index = 0
        self.__add_existing = False
        self.__selected_row = IntVar(self.parent)
        self.__selected_row.set(0)

        self.scenario_description = u''
        self.scenario_description_var = StringVar(self.parent)

        self.scenario_radio_list = {}
        self.scenario_library_list = {}
        self.scenario_library_var_list = {}
        self.scenario_library_tooltip_list = {}
        self.scenario_modifier_list = {}
        self.scenario_modifier_tooltip_list = {}
        self.scenario_modifier_var_list = {}
        self.scenario_filter_list = {}
        self.scenario_filter_var_list = {}
        self.sceanrio_override_list = {}
        self.scenario_override_var_list = {}
        self.scenario_parameter_list = {}
        self.scenario_parameter_var_list = {}
        self.scenario_active_list = {}
        self.scenario_active_var_list = {}

        self.existing_scenarios = [scenario[ScenarioConstant.name] for scenario in self._scenarios.get_items()]
        self.existing_scenarios.sort()

        if selected_scenario:
            self.selected_scenario = selected_scenario

        elif self.edit:
            self.selected_scenario = self._cfg.selected_scenario  # This is the active scenario

        else:
            self.selected_scenario = None

        label_column = self.column.start()
        entry_column = self.column.next()

        self.label(text=u'Scenario Name:',
                   row=self.row.next(),
                   column=label_column,
                   sticky=W)

        self.__scenario_name_var = StringVar(self.parent)
        self.__scenario_name_var.set(self.selected_scenario if self.edit else u'')
        self.__scenario_name, _ = self.combobox(textvariable=self.__scenario_name_var,
                                                values=self.existing_scenarios,
                                                state=DISABLED if self.edit else NORMAL,
                                                row=self.row.current,
                                                column=entry_column,
                                                sticky=EW,
                                                columnspan=6,
                                                tooltip=(u'Add your own scenario or select '
                                                         u'from a list of pre-defined scenarios!'))

        self.__scenario_name.bind(u'<<ComboboxSelected>>',
                                  self.__populate_scenario)
        self.__scenario_name.bind(u'<Return>',
                                  self.__populate_scenario)
        self.__scenario_name.bind(u'<Tab>',
                                  self.__populate_scenario)

        self.SCENARIO_DESCR_COL = self.column.start()
        self.SCENARIO_DESCR_ROW = self.row.next()
        self.__build_description_frame()

        self.separator(orient=HORIZONTAL,
                       row=self.row.next(),
                       column=label_column,
                       columnspan=7,
                       sticky=EW,
                       padx=5,
                       pady=5)

        self.label(text=u'Scenario Config:',
                   row=self.row.next(),
                   column=label_column,
                   sticky=W)

        self.SCENARIO_CONFIG_COL = self.column.start()
        self.SCENARIO_CONFIG_ROW = self.row.next()
        self._build_scenario_config_frame()

        self.separator(orient=HORIZONTAL,
                       row=self.row.next(),
                       column=label_column,
                       columnspan=7,
                       sticky=EW,
                       padx=5,
                       pady=5)


        self.__add_config_row_button = self.button(state=NORMAL,
                                                   text=u'+',
                                                   width=5,
                                                   command=self.__add_row,
                                                   row=self.row.next(),
                                                   column=self.column.start())

        self.__move_up_row_button = self.button(state=NORMAL,
                                                text=u'▲',
                                                width=5,
                                                command=self.__move_up,
                                                column=self.column.next())

        self.__move_down_row_button = self.button(state=NORMAL,
                                                  text=u'▼',
                                                  width=5,
                                                  command=self.__move_down,
                                                  column=self.column.next(),
                                                  sticky=W)
        self.columnconfigure(self.column.current, weight=1)

        self.__pickle_button = self.button(state=NORMAL,
                                           text=u'Pickler',
                                           width=15,
                                           command=self.launch_pickler,
                                           column=self.column.next())

        self.columnconfigure(self.column.current, weight=1)

        self.__cancel_button = self.button(state=NORMAL,
                                           text=u'Cancel',
                                           width=15,
                                           command=self.cancel,
                                           column=self.column.next())

        self.__push_button = self.button(state=NORMAL,
                                         text=(u'Push'
                                               if self.edit
                                               else u'Add & Push'),
                                         width=15,
                                         command=self.__push,
                                         column=self.column.next())

        self.__save_button = self.button(state=NORMAL,
                                         text=(u'Save'
                                               if self.edit
                                               else u'Add'),
                                         width=15,
                                         command=(self.__save
                                                  if self.edit
                                                  else self.__save),
                                         column=self.column.next())
        #self.nice_grid()

    def __get_description(self):
        return self.scenario_description_var.get()

    def __get_loaded_config(self):

        cfg = []

        for i in range(self.index):
            # Get config parameters
            config_param = {
                ModifierConstant.handler: self.scenario_library_var_list[i].get(),
                ModifierConstant.modifier: self.scenario_modifier_var_list[i].get(),
                ModifierConstant.active: (True
                                          if self.scenario_active_var_list[i].get() == 1
                                          else False),
                ModifierConstant.filter: self.scenario_filter_var_list[i].get(),
                ModifierConstant.override: self.scenario_override_var_list[i].get(),
                ModifierConstant.params: self.scenario_parameter_var_list[i].get()
            }

            cfg.append(config_param)

        return cfg

    def __update_scenario(self):

        updated_modifiers = []

        # (Re)Insert all rows
        for i in range(self.index):

            modifier_row = {
                ModifierConstant.handler: self.scenario_library_var_list[i].get(),
                ModifierConstant.modifier: self.scenario_modifier_var_list[i].get(),
                ModifierConstant.active: self.scenario_active_var_list[i].get(),
                ModifierConstant.filter: self.scenario_filter_var_list[i].get(),
                ModifierConstant.override: self.scenario_override_var_list[i].get(),
                ModifierConstant.params: self.scenario_parameter_var_list[i].get()
            }

            if not self.__check_if_row_blank(modifier_row):
                updated_modifiers.append(modifier_row)

        if self.edit:
            scenario = self._scenarios.get_item(self.selected_scenario)
            scenario.description = self.scenario_description_var.get()

            scenario.modifiers = updated_modifiers
            scenario.save_changes()

        else:
            new_scenario = {
                ScenarioConstant.description: self.scenario_description_var.get(),
                ScenarioConstant.modifiers: updated_modifiers
            }

            self._scenarios.add(key_attr=self.__scenario_name.get(),
                                config=new_scenario)

    def launch_pickler(self):
        window = RequestPicklerWindow(
                parent_geometry=(self.parent
                                 .winfo_toplevel()
                                 .winfo_geometry()))
        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

    def __push(self):
        self.__update_scenario()
        self.intercept_server.reload_config()

        if not self.edit:
            self.__scenario_name.config(state=DISABLED)
            self.__push_button.config(text=u'Push')
            self.__save_button.config(text=u'Save')

            self.edit = True

    def __save(self):
        self.__update_scenario()
        self.parent.master.exit()

    def cancel(self):
        self.parent.master.exit()

    def _build_scenario_config_frame(self):

        self.scenario_config_frame = BaseFrame(self)
        frame = self.scenario_config_frame
        frame.grid(row=self.SCENARIO_CONFIG_ROW,
                   column=self.SCENARIO_CONFIG_COL,
                   columnspan=7,
                   sticky=NSEW,
                   padx=20)

        frame.RADIO_COLUMN = frame.column.next()
        frame.LIB_ENTRY_COLUMN = frame.column.next()
        frame.MOD_ENTRY_COLUMN = frame.column.next()
        frame.FIL_ENTRY_COLUMN = frame.column.next()
        frame.OVR_ENTRY_COLUMN = frame.column.next()
        frame.PAR_ENTRY_COLUMN = frame.column.next()
        frame.ACT_ENTRY_COLUMN = frame.column.next()

        self.scenario_config_frame.HEADER_ROW = self.scenario_config_frame.row.next()

        for text, col in ((u'Library',    frame.LIB_ENTRY_COLUMN),
                          (u'Modifier',   frame.MOD_ENTRY_COLUMN),
                          (u'Filter',     frame.FIL_ENTRY_COLUMN),
                          (u'Override',   frame.OVR_ENTRY_COLUMN),
                          (u'Parameters', frame.PAR_ENTRY_COLUMN),
                          (u'Active',     frame.ACT_ENTRY_COLUMN),):

            frame.label(text=text,
                        row=frame.HEADER_ROW,
                        column=col)

        frame.separator(orient=HORIZONTAL,
                        row=frame.row.next(),
                        column=frame.RADIO_COLUMN,
                        columnspan=7,
                        sticky=EW,
                        padx=5,
                        pady=5)

        if self.index == 0:

            if self.edit:
                scenario = self._scenarios.get_item(self.selected_scenario)

                for mod in scenario.modifiers:
                    self.__build_row(index=self.index,
                                     cfg=mod)
                    self.index += 1

            # Add new empty row
            self.__build_row(index=self.index)
            self.index += 1

        else:
            # Rebuild if config already loaded (needed for moving rows up/down)
            config = [self.__get_loaded_config()[i]
                      for i in range(0, len(self.__get_loaded_config()))]
            self.index = 0

            for cfg in config:
                self.__build_row(index=self.index,
                                 cfg=cfg)
                self.index += 1

        nice_grid(self.scenario_config_frame)

    def update_library_tooltip(self,
                               index):
        # TODO: Handle 'Scenario'
        try:
            config = self.__get_loaded_config()[index]
            handler = config[ModifierConstant.handler]

            if handler == u'Scenario':
                return self.update_modifier_tooltip(index)

        except Exception as e:
            return e.message

        try:
            doc = self._modifiers.handlers[handler][ModifierConstant.module].__doc__
            logging.debug(doc)
            return doc if doc else self.update_modifier_tooltip(index)

        except KeyError:
            if not handler:
                return u'No Handler specified'

            return u'{handler} is not recognised'.format(handler=handler)

    @staticmethod
    def scenario_tooltip_description(scenario):
        # TODO:Get the description from the scenario
        return u'Runs the {scenario} scenario'.format(scenario=scenario)

    def update_modifier_tooltip(self,
                                index):
        # TODO: Handle 'Scenario'
        try:
            config = self.__get_loaded_config()[index]
            handler = config[ModifierConstant.handler]
            modifier = config[ModifierConstant.modifier]

        except Exception as e:
            return e.message

        try:
            mod = u'{handler}.{modifier}'.format(handler=handler,
                                                 modifier=modifier)

            if modifier and handler == u'Scenario':
                return self.scenario_tooltip_description(scenario=modifier)

            return make_modifier_tooltip_from_docstring(mod=self._modifiers[mod][ModifierConstant.module])

        except KeyError:
            if not handler:
                return u'No Handler specified'

            if not modifier:
                return u'No Modifier specifier'

            return u'{handler}/{modifier} is not a valid combination'.format(handler=handler,
                                                                             modifier=modifier)

    def __build_row(self, index, cfg=None):

            config_row = self.scenario_config_frame.row.next()

            self.scenario_radio_list[index] = self.scenario_config_frame.radiobutton(
                    variable=self.__selected_row,
                    value=int(index),
                    row=config_row,
                    column=self.scenario_config_frame.RADIO_COLUMN,
                    sticky=W)

            self.scenario_library_var_list[index] = StringVar(self.parent)

            self.scenario_library_var_list[index].set(cfg[ModifierConstant.handler] if cfg else u'')

            (self.scenario_library_list[index],
             self.scenario_library_tooltip_list[index]) = self.scenario_config_frame.combobox(
                    textvariable=self.scenario_library_var_list[index],
                    postcommand=lambda: self.__populate_handlers(
                                          self.scenario_library_list[index]),
                    row=config_row,
                    column=self.scenario_config_frame.LIB_ENTRY_COLUMN,
                    sticky=EW,
                    tooltip={u'text': self.update_library_tooltip,
                             u'index': index})

            self.scenario_modifier_var_list[index] = StringVar(self.parent)
            self.scenario_modifier_var_list[index].set(cfg[ModifierConstant.modifier] if cfg else u'')

            (self.scenario_modifier_list[index],
             self.scenario_modifier_tooltip_list[index]) = self.scenario_config_frame.combobox(
                    textvariable=self.scenario_modifier_var_list[index],
                    postcommand=(lambda:
                                 self.__populate_modifiers(
                                     self.scenario_modifier_list[index],
                                     self.scenario_library_var_list[index])),
                    row=config_row,
                    column=self.scenario_config_frame.MOD_ENTRY_COLUMN,
                    sticky=EW,
                    tooltip={u'text':  self.update_modifier_tooltip,
                             u'index': index,
                             u'font':  (u"courier", u"10", u"normal")})

            self.scenario_filter_var_list[index] = StringVar(self.parent)
            self.scenario_filter_var_list[index].set(cfg[ModifierConstant.filter] if cfg else u'')

            self.scenario_filter_list[index] = self.scenario_config_frame.entry(
                    textvariable=self.scenario_filter_var_list[index],
                    row=config_row,
                    column=self.scenario_config_frame.FIL_ENTRY_COLUMN,
                    sticky=EW)

            self.scenario_override_var_list[index] = StringVar(self.parent)
            self.scenario_override_var_list[index].set(cfg[ModifierConstant.override] if cfg else u'')

            self.sceanrio_override_list[index] = self.scenario_config_frame.entry(
                    textvariable=self.scenario_override_var_list[index],
                    row=config_row,
                    column=self.scenario_config_frame.OVR_ENTRY_COLUMN,
                    sticky=EW)

            self.scenario_parameter_var_list[index] = StringVar(self.parent)
            self.scenario_parameter_var_list[index].set(cfg[ModifierConstant.params] if cfg else u'')

            self.scenario_parameter_list[index] = self.scenario_config_frame.entry(
                    textvariable=self.scenario_parameter_var_list[index],
                    width=50,
                    row=config_row,
                    column=self.scenario_config_frame.PAR_ENTRY_COLUMN,
                    sticky=EW)

            active = 0

            if cfg:
                if cfg[ModifierConstant.active]:
                    active = 1

            self.scenario_active_var_list[index] = BooleanVar(self.parent)
            self.scenario_active_var_list[index].set(active)
            self.scenario_active_list[index] = self.scenario_config_frame.checkbutton(
                    variable=self.scenario_active_var_list[index],
                    row=config_row,
                    column=self.scenario_config_frame.ACT_ENTRY_COLUMN)

    def __build_description_frame(self):

        self.scenario_description_frame = BaseFrame(self)
        frame = self.scenario_description_frame
        frame.grid(row=self.SCENARIO_DESCR_ROW,
                   column=self.SCENARIO_DESCR_COL,
                   columnspan=7,
                   sticky=EW,
                   padx=0)

        frame.LABEL_COLUMN = frame.column.start()
        frame.ENTRY_COLUMN = frame.column.next()
        frame.columnconfigure(frame.ENTRY_COLUMN, weight=1)

        frame.HEADER_ROW = frame.row.next()

        if self.selected_scenario is None:
            description = u''

        else:
            scenario = self._scenarios.get_item(self.selected_scenario)
            description = scenario.description

        self.__build_description_row(description=description)

    def __build_description_row(self,
                                description=None):

        description_row = self.scenario_description_frame.row.next()

        self.scenario_description_frame.label(text=u'Description:',
                                              width=19,
                                              row=description_row,
                                              column=self.scenario_description_frame.LABEL_COLUMN,
                                              sticky=W)

        self.scenario_description_var.set(description)

        self.scenario_description = self.scenario_description_frame.entry(
                textvariable=self.scenario_description_var,
                row=description_row,
                column=self.scenario_description_frame.ENTRY_COLUMN,
                sticky=EW,
                columnspan=3)

    def __add_row(self):
        self.__build_row(index=self.index)
        self.index += 1
        self.nice_grid()

        self.parent.master.update_geometry()

    def __move_up(self):

        current = self.__selected_row.get()

        if not current == 0:
            new = current - 1

            for column_list in (self.scenario_radio_list,
                                self.scenario_library_list,
                                self.scenario_library_var_list,
                                self.scenario_modifier_list,
                                self.scenario_modifier_var_list,
                                self.scenario_filter_list,
                                self.scenario_filter_var_list,
                                self.sceanrio_override_list,
                                self.scenario_override_var_list,
                                self.scenario_parameter_list,
                                self.scenario_parameter_var_list,
                                self.scenario_active_list,
                                self.scenario_active_var_list):

                column_list[u'x'] = column_list[current]
                column_list[current] = column_list[new]
                column_list[new] = column_list[u'x']
                del column_list[u'x']

            self.scenario_config_frame.destroy()
            self._build_scenario_config_frame()

            self.__selected_row.set(new)

    def __move_down(self):

        current = self.__selected_row.get()

        if not current == (len(self.scenario_radio_list) - 1):
            new = current + 1

            for column_list in (self.scenario_radio_list,
                                self.scenario_library_list,
                                self.scenario_library_var_list,
                                self.scenario_modifier_list,
                                self.scenario_modifier_var_list,
                                self.scenario_filter_list,
                                self.scenario_filter_var_list,
                                self.sceanrio_override_list,
                                self.scenario_override_var_list,
                                self.scenario_parameter_list,
                                self.scenario_parameter_var_list,
                                self.scenario_active_list,
                                self.scenario_active_var_list):

                column_list[u'x'] = column_list[current]
                column_list[current] = column_list[new]
                column_list[new] = column_list[u'x']
                del column_list[u'x']

            self.scenario_config_frame.destroy()
            self._build_scenario_config_frame()

            self.__selected_row.set(new)

    def __populate_scenario(self,
                            event):  # event is required as a parameter
        #                            # the bind function passes in.
        self.selected_scenario = self.__scenario_name.get()

        # If there is an existing scenario
        if self.selected_scenario in self.existing_scenarios:
            self.index = 0
            self.edit = True
            self.__add_existing = True
            self.__save_button.config(text=u'Save',
                                      command=self.__save)

            self.scenario_description_frame.destroy()
            self.__build_description_frame()

            self.scenario_config_frame.destroy()
            self._build_scenario_config_frame()

        # If no existing scenario
        else:
            self.edit = False
            self.__add_existing = False
            self.__save_button.config(text=u'Add',
                                      command=self.__save)

            # If scenario name is cleared reset all fields
            if not self.selected_scenario:
                self.index = 0
                self.scenario_config_frame.destroy()
                self._build_scenario_config_frame()

                self.scenario_description_frame.destroy()
                self.__build_description_frame()

    def __populate_handlers(self, combo):

        handlers = [handler.name
                    for handler in self._handlers.get_items()] + [u'Scenario']

        handlers.sort()

        logging.debug(handlers)

        combo.config(values=handlers)

    def __populate_modifiers(self, combo, selected_handler):

        handler = selected_handler.get()

        if handler.lower() == u'scenario':
            modifiers = self.existing_scenarios

        else:

            modifiers = [modifier[ModifierConstant.modifier_name]
                         for modifier in self._modifiers.registered_modifiers.values()
                         if handler == modifier[ModifierConstant.handler]]

        modifiers.sort()
        logging.debug(modifiers)

        combo.config(values=modifiers)

    def __populate_filters(self,
                           combo,
                           selected_handler,
                           selected_modifier):
        # TODO: Populate this
        _ = self  # this removes the staticmethod warning until this is populated!
        return []

    @staticmethod
    def trim(dir_list):
        return filter_list(item_list=dir_list,
                           filters=[u'__init__', u'.pyc', u'handler'],
                           exclude=True)

    @staticmethod
    def __check_if_row_blank(config):

        blank = True

        for item in config.values():
            if item not in [u'', False]:
                blank = False

        return blank
