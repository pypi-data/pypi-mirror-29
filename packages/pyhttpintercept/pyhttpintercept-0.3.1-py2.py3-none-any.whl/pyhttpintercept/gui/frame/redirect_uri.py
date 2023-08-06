# encoding: utf-8

import logging_helper
from tableutil import Table
from collections import OrderedDict
from uiutil.frame import BaseFrame
from uiutil.widget.label import Label
from uiutil.widget.button import Button
from uiutil.widget.combobox import Combobox
from configurationutil import Configuration
from tkinter.messagebox import showerror
from tkinter.constants import NORMAL, DISABLED, E, EW
from networkutil.endpoint_config import Endpoints, EnvAndAPIs
from fdutil.string_tools import make_multi_line_list
from ...config import redirect


logging = logging_helper.setup_logging()

TRANSPARENT = u'Transparent'


class AddEditRedirectURIFrame(BaseFrame):

    DEFAULT_REDIRECT = u''

    def __init__(self,
                 selected_record=None,
                 edit=False,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self,
                           *args,
                           **kwargs)

        self.edit = edit

        self.cfg = Configuration()

        self.endpoints = Endpoints()
        self.env_and_apis = EnvAndAPIs()

        try:
            key = u'{cfg}.{h}'.format(cfg=redirect.REDIRECT_CFG,
                                      h=selected_record)

            self.selected_config = self.cfg[key]

        except LookupError:
            self.selected_host = None
            self.selected_config = None

        else:
            self.selected_host = selected_record

        self._draw()

    def _draw(self):

        Label(text=u'URI:',
              row=self.row.next(),
              column=self.column.start(),
              sticky=E,
              tooltip=self.tooltip)

        existing_redirects = redirect.get_redirection_config().keys()

        # TODO: necessary?  Do we want the hassle of friendly names here?
        host_endpoints = set([endpoint.hostname for endpoint in self.endpoints])
        host_endpoints = list(host_endpoints.difference(existing_redirects))
        host_endpoints = sorted(host_endpoints)

        initial_uri = host_endpoints[0] if len(host_endpoints) > 0 else u''

        self._uri = Combobox(frame=self,
                             value=self.selected_host if self.edit else initial_uri,
                             values=host_endpoints,
                             state=DISABLED if self.edit else NORMAL,
                             row=self.row.current,
                             column=self.column.next(),
                             sticky=EW,
                             columnspan=3)

        self.columnconfigure(self.column.current, weight=1)

        Label(text=u'Redirect URI:',
              row=self.row.next(),
              column=self.column.start(),
              sticky=E,
              tooltip=self.tooltip)

        self._redirect = Combobox(frame=self,
                                  value=self.selected_config[redirect.URI]
                                  if self.edit else u'',
                                  state=NORMAL,
                                  row=self.row.current,
                                  column=self.column.next(),
                                  sticky=EW,
                                  columnspan=3)

        self.populate_redirect_list()

        self.rowconfigure(self.row.current, weight=1)

        Label(text=u'Status:',
              row=self.row.next(),
              column=self.column.start(),
              sticky=E,
              tooltip=self.tooltip)

        initial_status = TRANSPARENT

        if self.edit:
            if self.selected_config[redirect.STATUS]:
                initial_status = self.selected_config[redirect.STATUS]

        self._status = Combobox(frame=self,
                                initial_value=initial_status,
                                values=[
                                    TRANSPARENT,
                                    301,
                                    302,
                                    303,
                                    307,
                                    308
                                ],
                                row=self.row.current,
                                column=self.column.next(),
                                sticky=EW,
                                columnspan=3)

        self.horizontal_separator(row=self.row.next(),
                                  column=self.column.start(),
                                  columnspan=4,
                                  sticky=EW,
                                  padx=5,
                                  pady=5)

        self._cancel_button = Button(text=u'Cancel',
                                     width=15,
                                     command=self._cancel,
                                     row=self.row.next(),
                                     column=self.column.next())

        self._save_button = Button(text=u'Save',
                                   width=15,
                                   command=self._save,
                                   row=self.row.current,
                                   column=self.column.next())

    def _save(self):
        redirect_host = self._uri.value
        redirect_name = self._redirect.value
        redirect_status = self._status.value

        logging.debug(redirect_host)
        logging.debug(redirect_name)

        try:
            if redirect_name.strip() == u'':
                raise Exception(u'redirect URI cannot be blank!')

            self._convert_friendly_name_to_host(host=redirect_host,
                                                name=redirect_name)

            values = {redirect.URI: redirect_name,
                      redirect.STATUS: None if redirect_status == TRANSPARENT else int(redirect_status),
                      redirect.ACTIVE: self.selected_config[redirect.ACTIVE] if self.edit else False}

            key = u'{cfg}.{h}'.format(cfg=redirect.REDIRECT_CFG,
                                      h=redirect_host)

            logging.debug(values)

            self.cfg[key] = values

            self.parent.master.exit()

        except Exception as err:
            logging.error(u'Cannot save record')
            logging.exception(err)
            showerror(title=u'Save Failed',
                      message=u'Cannot Save redirect URI: {err}'.format(err=err))

    def _cancel(self):
        self.parent.master.exit()

    def populate_redirect_list(self):
        uri = self._uri.value
        redirect_uri = self._redirect.value

        try:
            host_apis = self.endpoints.get_apis_for_host(uri)

            redirect_environments = set()

            for host_api in host_apis:
                redirect_environments.update(set(self.env_and_apis.get_environments_for_api(host_api)))

            redirect_environments.add(self.DEFAULT_REDIRECT)

            # Check for a friendly name for host
            friendly_name = self._convert_host_to_friendly_name(uri)

            if friendly_name is not None:
                redirect_environments.remove(friendly_name)

            redirect_environments = sorted(list(redirect_environments))

            try:
                redirect_hostname = self.selected_config[redirect.URI]

                endpoint = [endpoint
                            for endpoint in self.endpoints
                            if endpoint.hostname == redirect_hostname
                            ][0]

                if endpoint.hostname == uri:
                    env = self.DEFAULT_REDIRECT

                else:
                    env = endpoint.environment

            except (IndexError, TypeError):
                if self.edit:
                    redirect_environments.append(redirect_uri)

                env = redirect_uri if self.edit else self.DEFAULT_REDIRECT

            self._redirect.config(values=redirect_environments)
            self._redirect.current(redirect_environments.index(env))
            self._redirect.set(env)

        except KeyError:
            logging.error(u'Cannot load redirect list, Invalid hostname!')

    @property
    def tooltip(self):

        tooltip_text = u"Examples:\n"

        example = OrderedDict()
        example[u'URI'] = u'google.com'
        example[u'Redirect URI'] = u'google.co.uk'
        example[u'Status'] = u'301'

        tooltip_text += Table.init_from_tree(example,
                                             title=make_multi_line_list(u"requests for 'google.com' "
                                                                        u"are diverted to 'google.co.uk' "
                                                                        u"using a HTTP 301 Permanent redirect."),
                                             table_format=Table.LIGHT_TABLE_FORMAT).text() + u'\n'

        return tooltip_text

    @staticmethod
    def _convert_host_to_friendly_name(host):

        try:
            # Attempt to lookup friendly name
            return Endpoints().get_environment_for_host(host)

        except LookupError:
            logging.debug(u'No friendly name available for host: {host}'.format(host=host))
            return None

    @staticmethod
    def _convert_friendly_name_to_host(host,
                                       name):

        endpoints = Endpoints()

        apis = endpoints.get_apis_for_host(host)
        logging.debug(apis)

        for api in apis:
            try:
                matched_endpoint = endpoints.get_endpoint_for_api_and_environment(
                    api=api,
                    environment=name)

                logging.debug(matched_endpoint)

                name = matched_endpoint.hostname
                break  # We got one!

            except ValueError:
                pass

        return name
