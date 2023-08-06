# csvtsdb
CSV-backed timeseries database. Usable standalone or in a Twisted application.

Not your typical timeseries database:

|                   |                    |
|-------------------|--------------------|
| Fast              | :x:                |
| Good compression  | :x:                |
| **Stupid simple** | :heavy_check_mark: |

Implies you probably don't want to use it unless you know you do. A good use case is for small amounts of data that should be easily editable and/or readable in 30 years when your favorite real TSDB software is long dead.

I will use it in my personal tracking project (TBA), which expects about 1 datapoint per series per day (and a small number of series), because most datapoints are input by the user.
