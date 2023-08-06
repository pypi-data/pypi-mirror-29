# encoding: utf-8

import logging_helper
from ..config.hosting import Sites
from ..methods.shared import RequestShared

logging = logging_helper.setup_logging()


class HostRequest(RequestShared):

    def __init__(self,
                 *args,
                 **kwargs):

        super(HostRequest, self).__init__(*args,
                                          **kwargs)

        self.hosted = False

    # Hosting
    def host_request(self):

        try:
            # Check is site is configured
            site = Sites().get_active_item(self.request_path)

            # If we haven't raised a LookupError then site is configured to host the request
            self.__handle_host_request(site)

        except LookupError:
            # Check for server test page
            if self.request_path == u'/test':
                self.__server_test_page()

            # No sites or static pages found.
            else:
                logging.debug(self.prefix_message(u'Not Hosting this request, '
                                                  u'path is either disabled or not configured.'))

        return self.response, self.hosted

    def __handle_host_request(self,
                              site):
        logging.debug(self._get_debug_separator(u'HOST REQUEST'))

        logging.debug(self.prefix_message(site.doc_root))

        # TODO: Need to handle serving the hosted site here
        # Start by handling the index.html
        # Once that is working we should look at decoding sub pages within the site!

        # ### Temporary response! ###
        msg = u'Hosting is not yet supported on this server! ({url})'.format(url=self.request_uri)
        self.__handle_error(err=msg,
                            status=501,  # Not Implemented
                            log_msg=msg)
        # ### End temporary response ###

        self.hosted = True  # Flag that the request has been hosted

        logging.debug(self._get_debug_separator(u'END HOST REQUEST'))

    def __server_test_page(self):

        logging.debug(self._get_debug_separator(u'SERVER TEST PAGE'))

        # Prepare response
        self.response.content = (u'<h1>Server Test Page</h1>'
                                 u'<p>you have requested {uri}</p>'
                                 u'<pre>Congratulations the server is working!</pre>'
                                 .format(uri=self.request_uri))

        self.response.status = 200
        self.response.headers = {u'Content-Type': u'text/html',
                                 u'content-length': len(self.response.content)}

        self.hosted = True  # Flag that the request has been hosted

        logging.debug(self._get_debug_separator(u'END SERVER TEST PAGE'))
