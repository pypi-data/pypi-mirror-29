#!/usr/bin/env python3

from . import CsvTsdb

FILE    = './data.csv'
PORT    = 8500

CsvTsdb(FILE).app.run(endpoint_description=r'tcp6:port={}:interface=\:\:'.format(PORT))  # bind to v6 and v4
