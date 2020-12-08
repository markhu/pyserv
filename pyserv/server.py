#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
class bcolors:
    BOLD = '\033[1m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m' ; OKGREEN_BOLD = OKGREEN + BOLD
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'
    
class S(BaseHTTPRequestHandler):
    def _set_response(self,log_more=''):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        logging.info(f"{bcolors.OKGREEN_BOLD}{self.command} {self.path}{bcolors.ENDC}")
        logging.info("Headers:\n%s\n%s" % (str(self.headers), log_more))
        return self

    def do_GET(self):
        self._set_response()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length",0))  # incoming data-size (advisory)
        post_data = self.rfile.read(content_length)
        self._set_response(log_more="Body:%s" % post_data)
        self.wfile.write(f"{self.command} Content-Length: {content_length}".encode('utf-8'))

    do_PUT = do_POST


def run_server(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    
    for try_port in range(port, port+50):
        try :
            server_address = ('', try_port)
            httpd = server_class(server_address, handler_class)
            break
        except OSError:
            logging.info(f"{bcolors.WARNING}PORT {try_port} unavailable. Trying PORT {try_port+1}{bcolors.ENDC}")

    logging.info(f'{bcolors.OKGREEN}Starting HTTP SERVER at PORT {try_port}{bcolors.ENDC}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info('Stopping httpd on port %s\n' % try_port)


if __name__ == '__main__':
    import sys
    port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port=port)
