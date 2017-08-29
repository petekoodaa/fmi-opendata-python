import datetime
import os
import requests
import sys
import xml.etree.cElementTree as ET

class FMIError(Exception):
    """Raise when the FMI data query fails."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class NamedTimeSeries:
    """Data structure representing named time series data."""
    def __init__(self):
        self.name = ''
        self.t = []
        self.data = []

class FMIOpenData:
    def __init__(self):
        try:
            self.apikey = os.environ["fmiapikey"]
        except KeyError:
            print "Please set the environment variable fmiapikey"
            raise

    def get_data(self, location, parameter, starttime='', endtime=''):
        """Get the data.

        Args:
        location -- location for the query (e.g. 'Helsinki')
        parameter -- comma separated string of measurement parameters
                     (e.g. 'temperature,pressure,dewpoint')
        starttime -- UTC starttime for the query (if omitted, data is queried
                     from the latest even 10 minute time stamp, e.g. 10:20:00)
        endtime -- UTC endtime for the query (if omitted, data is queried up to
                   the current time)

        Returns:
        data -- received data as a NamedTimeSeries list
        """

        query = 'http://data.fmi.fi/fmi-apikey/{}/wfs?request=getFeature' \
            '&storedquery_id=fmi::observations::weather::timevaluepair' \
            '&place={}' \
            '&parameters={}'.format(self.apikey, location, parameter)

        if not starttime:
            tm = datetime.datetime.utcnow()
            tm = tm - datetime.timedelta(minutes=tm.minute % 10,
                seconds=tm.second,
                microseconds=tm.microsecond)
            starttime = tm.strftime("%Y-%m-%dT%H:%M:%SZ")

        query += '&starttime={}'.format(starttime)

        if endtime:
            query += '&endtime={}'.format(endtime)

        r = requests.get(query)

        if r.status_code != 200:
            raise(FMIError(r.content))

        return self._parse_data_tree(ET.fromstring(r.content))

    def _parse_data_tree(self, tree):
        alldata = []

        measurements = []
        for elem in tree.iter('{http://www.opengis.net/waterml/2.0}MeasurementTimeseries'):
            measurements.append(elem)

        for meas in measurements:
            data = NamedTimeSeries()

            data.name = meas.attrib['{http://www.opengis.net/gml/3.2}id'].split("-")[-1]

            for timepoint in meas.iter('{http://www.opengis.net/waterml/2.0}time'):
                data.t.append(datetime.datetime.strptime(timepoint.text, "%Y-%m-%dT%H:%M:%SZ"))

            for datapoint in meas.iter('{http://www.opengis.net/waterml/2.0}value'):
                data.data.append(float(datapoint.text))

            alldata.append(data)

        return alldata
