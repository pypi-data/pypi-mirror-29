# csvtsdb
CSV-backed timeseries database. Usable standalone or in a Twisted application.

[![PyPI](https://img.shields.io/pypi/v/csvtsdb.svg)](https://pypi.org/project/csvtsdb/)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/AnotherKamila)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/anotherkamila/songbook-web/issues)


Not your typical timeseries database:

|                   |                    |
|-------------------|--------------------|
| Fast              | :x:                |
| Good compression  | :x:                |
| **Stupid simple** | :heavy_check_mark: |

Implies you probably don't want to use it unless you know you do. A good use case is for _small amounts of data_ that should be _easily editable and/or readable in 30 years_ when your favorite real TSDB software is long dead.

I will use it in my personal tracking project (TBA), which expects about 1 datapoint per series per day (and a small number of series), because most datapoints are input by the user.

**Note**: if you want to use this, but you are not happy with the request format (e.g. you want JSON), [let me know](https://github.com/AnotherKamila/csvtsdb/issues/new) -- that is a very easy change.

This is a WIP and it will have more features in the future.
