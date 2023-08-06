# encoding: utf-8

import os
import sys
import time
import logging_helper
from pydnserver import DNSServer
from pyhttpintercept.server import (ThreadedHTTPWebServer,
                                    HTTPWebServer,
                                    HTTPRequestHandler)

logging = logging_helper.setup_logging()


class InterceptServer(object):

    DEFAULT_HTTP_PORTS = [80, ]
    DEFAULT_DNS_PORT = 53

    def __init__(self,
                 http_ports=DEFAULT_HTTP_PORTS,
                 dns_port=DEFAULT_DNS_PORT):

        self.http_ports = http_ports
        self.dns_port = dns_port

        self.http_server_instances = {}
        self.dns_server = None

    def start(self,
              threaded=True):

        if (sys.platform == u'darwin'
                and os.geteuid() != 0
                and any(port <= 1024 for port in self.http_ports + [self.dns_port])):
            raise Exception(u'You are running macOS please restart with sudo!')

        logging.info(u'Starting up, use <Ctrl-C> to stop!')

        # Start a HTTP server on each port in self.http_ports
        for http_port in self.http_ports:
            server_address = (u'', http_port)

            # Start HTTP Server
            server_class = ThreadedHTTPWebServer if threaded else HTTPWebServer
            request_handler_class = HTTPRequestHandler

            self.http_server_instances[http_port] = server_class(server_address=server_address,
                                                                 request_handler_class=request_handler_class)

            self.http_server_instances[http_port].start()
            time.sleep(1)

        # Start DNS Server
        self.dns_server = DNSServer(port=self.dns_port)
        self.dns_server.start()
        time.sleep(1)

        self.post_start_tasks()

        logging.info(u'Ready...')

    def stop(self):

        # Shutdown DNS Server
        if self.dns_server is not None:
            if self.dns_server.active:
                self.dns_server.stop()
                self.dns_server = None

        # Shutdown HTTP Server
        for http_server in self.http_server_instances.values():
            if http_server.active:
                http_server.stop()

        logging.info(u'Shut Down Complete')

    def reload_config(self):
        for http_server_instance in self.http_server_instances.values():
            http_server_instance.scenarios.reload_active_scenario()

    def post_start_tasks(self):
        pass
        # override to performs tasks after the servers have started
