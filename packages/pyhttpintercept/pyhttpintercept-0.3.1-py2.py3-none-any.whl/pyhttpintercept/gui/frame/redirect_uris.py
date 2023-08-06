# encoding: utf-8

import logging_helper
from tkinter import StringVar, BooleanVar
from tkinter.messagebox import askquestion
from tkinter.constants import HORIZONTAL, E, W, S, EW, NSEW
from uiutil.frame import BaseFrame
from uiutil.helper.layout import nice_grid
from configurationutil import Configuration
from networkutil.endpoint_config import Endpoints
from ...config import redirect
from ..window.redirect_uri import AddEditRedirectURIWindow

logging = logging_helper.setup_logging()


class RedirectURIConfigFrame(BaseFrame):

    def __init__(self,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self,
                           *args,
                           **kwargs)

        self._selected_record = StringVar(self.parent)

        self.cfg = Configuration()

        self.redirect_radio_list = {}
        self.redirect_active_var_list = {}
        self.redirect_active_list = {}

        self.columnconfigure(self.column.start(), weight=1)

        self.REDIRECT_ROW = self.row.next()
        self.rowconfigure(self.REDIRECT_ROW, weight=1)
        self.BUTTON_ROW = self.row.next()

        self._build_zone_frame()
        self._build_button_frame()

    def _build_zone_frame(self):

        self.record_frame = BaseFrame(self)
        self.record_frame.grid(row=self.REDIRECT_ROW,
                               column=self.column.current,
                               sticky=NSEW)

        self.record_frame.label(text=u'URI',
                                column=self.record_frame.column.start(),
                                sticky=W)
        self.rowconfigure(self.record_frame.column.current, weight=1)

        self.record_frame.label(text=u'Redirect URI',
                                column=self.record_frame.column.next(),
                                sticky=W)
        self.rowconfigure(self.record_frame.column.current, weight=1)

        self.record_frame.label(text=u'Status',
                                column=self.record_frame.column.next(),
                                sticky=W)

        self.record_frame.label(text=u'Active',
                                column=self.record_frame.column.next(),
                                sticky=W)

        self.record_frame.separator(orient=HORIZONTAL,
                                    row=self.record_frame.row.next(),
                                    column=self.record_frame.column.start(),
                                    columnspan=4,
                                    sticky=EW,
                                    padx=5,
                                    pady=5)

        for host, host_config in iter(redirect.get_redirection_config().items()):

            redirect_row = self.record_frame.row.next()

            if not self._selected_record.get():
                self._selected_record.set(host)

            self.redirect_radio_list[host] = self.record_frame.radiobutton(text=host,
                                                                           variable=self._selected_record,
                                                                           value=host,
                                                                           row=redirect_row,
                                                                           column=self.record_frame.column.start(),
                                                                           sticky=W)

            # Get the configured record
            text = host_config[u'uri']

            # Check for a friendly name for host
            friendly_name = self._convert_host_to_friendly_name(text)

            if friendly_name is not None:
                text = u'{name} ({host})'.format(name=friendly_name,
                                                 host=text)

            self.record_frame.label(text=text,
                                    row=redirect_row,
                                    column=self.record_frame.column.next(),
                                    sticky=W)

            self.record_frame.label(text=host_config[u'status'],
                                    row=redirect_row,
                                    column=self.record_frame.column.next(),
                                    sticky=W)

            self.redirect_active_var_list[host] = BooleanVar(self.parent)
            self.redirect_active_var_list[host].set(host_config[u'active'])

            self.redirect_active_list[host] = self.record_frame.checkbutton(
                variable=self.redirect_active_var_list[host],
                command=(lambda host=host,
                         flag=self.redirect_active_var_list[host]:
                         self._update_active(host=host,
                                             flag=flag)),
                row=redirect_row,
                column=self.record_frame.column.next(),
                sticky=W
            )

        self.record_frame.separator(orient=HORIZONTAL,
                                    row=self.record_frame.row.next(),
                                    column=self.record_frame.column.start(),
                                    columnspan=4,
                                    sticky=EW,
                                    padx=5,
                                    pady=5)

        nice_grid(self.record_frame)

    def _build_button_frame(self):

        button_width = 15

        self.button_frame = BaseFrame(self)
        self.button_frame.grid(row=self.BUTTON_ROW,
                               column=self.column.current,
                               sticky=(E, W, S))

        self.button(frame=self.button_frame,
                    name=u'_delete_record_button',
                    text=u'Delete Record',
                    width=button_width,
                    command=self._delete_uri_record,
                    row=self.button_frame.row.start(),
                    column=self.button_frame.column.start(),
                    tooltip=u'Delete\nselected\nrecord')

        self.button(frame=self.button_frame,
                    name=u'_add_record_button',
                    text=u'Add Record',
                    width=button_width,
                    command=self._add_uri_record,
                    row=self.button_frame.row.current,
                    column=self.button_frame.column.next(),
                    tooltip=u'Add record\nto dns list')

        self.button(frame=self.button_frame,
                    name=u'_edit_record_button',
                    text=u'Edit Record',
                    width=button_width,
                    command=self._edit_uri_record,
                    row=self.button_frame.row.current,
                    column=self.button_frame.column.next(),
                    tooltip=u'Edit\nselected\nrecord')

        nice_grid(self.button_frame)

    def _add_uri_record(self):
        window = AddEditRedirectURIWindow(fixed=True,
                                          parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

        self.record_frame.destroy()
        self._build_zone_frame()

        self.parent.master.update_geometry()

    def _edit_uri_record(self):
        window = AddEditRedirectURIWindow(selected_record=self._selected_record.get(),
                                          edit=True,
                                          fixed=True,
                                          parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

        self.record_frame.destroy()
        self._build_zone_frame()

        self.parent.master.update_geometry()

    def _delete_uri_record(self):
        result = askquestion(title=u"Delete Record",
                             message=u"Are you sure you "
                                     u"want to delete {r}?".format(r=self._selected_record.get()),
                             icon=u'warning',
                             parent=self)

        if result == u'yes':
            key = u'{c}.{h}'.format(c=redirect.REDIRECT_CFG,
                                    h=self._selected_record.get())

            del self.cfg[key]

            self.record_frame.destroy()
            self._build_zone_frame()

            self.parent.master.update_geometry()

    def _update_active(self,
                       host,
                       flag):
        key = u'{c}.{h}.{active}'.format(c=redirect.REDIRECT_CFG,
                                         h=host,
                                         active=redirect.ACTIVE)

        self.cfg[key] = flag.get()

    @staticmethod
    def _convert_host_to_friendly_name(host):

        try:
            # Attempt to lookup friendly name
            return Endpoints().get_environment_for_host(host)

        except LookupError:
            logging.debug(u'No friendly name available for host: {host}'.format(host=host))
            return None
