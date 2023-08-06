# encoding: utf-8

import logging_helper
from http.server import BaseHTTPRequestHandler
from classutils.decorators import profiling
from ..methods.get import GetHandler
from ..methods.post import PostHandler
from .._constants import PROFILER_PROFILE_ID

logging = logging_helper.setup_logging()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    BaseHTTPRequestHandler.protocol_version = u"HTTP/1.1"

    #  Override base class logging function
    def log_message(self,
                    fmt,
                    *args):
        logging.info(u"{addr} - {fmt}".format(addr=self.client_address[0],
                                              fmt=fmt % args))

    # Request handlers
    @profiling.profile(profile_id=PROFILER_PROFILE_ID)
    def do_GET(self):
        GetHandler(request=self,
                   scenarios=self.server.scenarios).handle()

    @profiling.profile(profile_id=PROFILER_PROFILE_ID)
    def do_POST(self):
        PostHandler(request=self,
                    scenarios=self.server.scenarios).handle()
