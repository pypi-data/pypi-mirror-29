#!/usr/bin/env python3
"""TODO docs
"""

import io
import json
from datetime import datetime, timezone

from klein               import Klein
from twisted.web.static  import File
from werkzeug.exceptions import NotFound, BadRequest

FILE    = './data.csv'
PORT    = 8500


class CsvTsdb():
    """TODO docs
    """
    GET_BYTES = 10*1024  # how many bytes to truncate to in GET requests

    app = Klein()

    def __init__(self, filename):
        self.filename = filename

    @app.route('/', methods=['POST'])
    def save(self, request):
        try:
            data = request.content.read().decode('utf-8')
            label, number = data.rsplit(maxsplit=1)
            number = float(number)
            if '"' in label: raise ValueError('label may not contain a " (double quote)')
            if ',' in label: raise ValueError('label may not contain a , (comma)')
        except ValueError as e:
            raise BadRequest(e) from e

        ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        csv_line = '{}, "{}", {}\n'.format(ts, label, number)
        with open(self.filename, 'a') as f:
            f.write(csv_line)

        request.setResponseCode(204)
        return None

    @app.route('/', methods=['GET'])
    def get(self, request):
        # TODO this should eventually do something else
        with open(self.filename, 'r') as f:
            f.seek(0, io.SEEK_END)
            end = f.tell()
            beg = max(0, end - self.GET_BYTES)
            f.seek(beg, io.SEEK_SET)
            f.readline() # eat stuff until next newline
            return f.read()  # for now this is synchronous because 10kb isn't that much


    @app.handle_errors(BadRequest)
    def handle_errors(self, request, failure):
        request.setResponseCode(failure.value.code)
        request.setHeader('Content-Type', 'text/plain')
        return failure.getErrorMessage()

    @property
    def resource(self):
        return self.app.resource()


if __name__ == '__main__':
    CsvTsdb(FILE).app.run(endpoint_description=r'tcp6:port={}:interface=\:\:'.format(PORT))  # bind to v6 and v4
