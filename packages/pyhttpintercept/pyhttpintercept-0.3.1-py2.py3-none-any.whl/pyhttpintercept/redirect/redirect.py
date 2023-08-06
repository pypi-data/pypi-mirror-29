# encoding: utf-8

import logging_helper
from ..config import redirect
from ..methods.shared import RequestShared

logging = logging_helper.setup_logging()


class RedirectRequest(RequestShared):

    def __init__(self,
                 *args,
                 **kwargs):

        super(RedirectRequest, self).__init__(*args,
                                              **kwargs)

        self.redirected = False

    # Redirect
    def redirect_request(self):

        try:
            # TODO: Breaks down when port supplied in request!
            # TODO: handle the returned redirect, transparent will act as below
            # TODO: if a status is present then we need to return response and skip any other actions!
            # TODO: add support for exact matching!

            active_redirects = redirect.get_active_redirection_config()
            matches = []

            for record in active_redirects:
                if self.request_uri.startswith(u'{protocol}://{record}'.format(protocol=self.request_protocol,
                                                                               record=record)):
                    matches.append(record)

            logging.debug(self.prefix_message(u'Redirect matches: {m}'.format(m=matches)))

            best_match_name = sorted(matches, key=len).pop()
            best_match = active_redirects[best_match_name]
            logging.debug(self.prefix_message(u'Redirect best match: {m}: {r}'.format(m=best_match_name,
                                                                                      r=best_match)))

            replace_len = len(self.request_protocol) + 3 + len(best_match_name)
            self.request_uri = u'{replace}{remaining}'.format(replace=best_match[redirect.URI],
                                                              remaining=self.request_uri[replace_len:])

            logging.info(self.prefix_message(u'Redirected URI: {uri}'.format(uri=self.request_uri)))
            self.redirected = True

        except IndexError:
            # index error catches pop() when there are no matches
            logging.debug(self.prefix_message(u'No redirects available!'))

        # TODO: need to pass back request URI!!

        return self.response, self.redirected
