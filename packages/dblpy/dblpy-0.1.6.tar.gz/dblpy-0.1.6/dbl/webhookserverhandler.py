#-*- coding:utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2018 Francis Taylor

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


import os
import logging
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


log = logging.getLogger(__name__)

AUTH_KEY = os.getenv('HOOK_AUTH', '')


class WebHook(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.headers.authorization[0] is not AUTH_KEY:
            log.info('Unauthorized request received, sending 403')
            self.send_error(403)
        else:
            log.info('Request received, sending 200')
            self.send_response(200)
        self.end_headers()

        length = int(self.headers['Content-Length'])
        post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
        payload = json.loads(post_data['payload'][0])

        return payload


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 330), WebHook)
    log.info(time.asctime, 'Webhook server start - {}:330'.format(hostName)

    try:
        server.serve_forever()
    except Exception as e:
        log.exception(e)

    server.server_close()
    log.info(time.asctime, 'Webhook server stop - {}:330'.format(hostName)
