# encoding: utf-8

import logging_helper
from .base import BaseRequestHandler


logging = logging_helper.setup_logging()


class GetHandler(BaseRequestHandler):
    METHOD_TYPE = u'GET'
