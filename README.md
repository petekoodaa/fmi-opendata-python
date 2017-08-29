# FMI-Opendata-Python

A minimal Python library to pull basic weather data from the FMI open data service.

## Motivation

I wanted a simple way to pull the temperature, pressure etc. data from selected cities. Could not find a suitable solution so I decided to write my own :)

## Prerequisites

Get a personal API key from [FMI](https://ilmatieteenlaitos.fi/avoin-data) to gain access to the FMI open data.

## Example uses

### Get the latest temperature from Helsinki

```
import fmiopendata

fmiod = fmiopendata.FMIOpenData()
fmidata = fmiod.get_data("Helsinki", "temperature")
```

### Get the temperature, pressure and visibility from Espoo with given start time

```
import fmiopendata

fmiod = fmiopendata.FMIOpenData()
fmidata = fmiod.get_data("Espoo", "temperature,pressure,visibility", "2017-08-29T07:00:00Z")
```

### Using the output

The data is currently returned as a list of custom objects (NamedTimeSeries). To print the data on the console:

```
for d in fmidata:
    print d.name, 'at', location
    for t, val in zip(d.t, d.data):
        print t.strftime("%Y-%m-%d %H:%M:%S"), val
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
