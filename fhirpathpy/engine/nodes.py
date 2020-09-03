import datetime
import json
import re
import time

dateFormat = '([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])'
timeRE = '([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\.[0-9]+)?'
dateTimeRE = '%s(T%s(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))?)?)?' % (dateFormat, timeRE)


class FP_Type:
    """
    Class FP_Type is the superclass for FHIRPath types that required special handling
    """

    def equals(self):
        """
        Tests whether this object is equal to another.  Returns either True,
        false, or undefined (where in the FHIRPath specification empty would be
        returned).  The undefined return value indicates that the values were the
        same to the shared precision, but that they had differnent levels of
        precision.
        """
        return False

    def equivalentTo(self):
        """
        Tests whether this object is equivalant to another.  Returns either True,
        false, or undefined (where in the FHIRPath specification empty would be
        returned).
        """
        return False

    def toString(self):
        return str(self)

    def toJSON(self):
        return str(self)

    def compare(self):
        raise NotImplementedError()


class FP_Quantity(FP_Type):
    """
    A map of the UCUM units that must be paired with integer values when doing arithmetic.
    """

    timeUnitsToUCUM = {
        "years": "'a'",
        "months": "'mo'",
        "weeks": "'wk'",
        "days": "'d'",
        "hours": "'h'",
        "minutes": "'min'",
        "seconds": "'s'",
        "milliseconds": "'ms'",
        "year": "'a'",
        "month": "'mo'",
        "week": "'wk'",
        "day": "'d'",
        "hour": "'h'",
        "minute": "'min'",
        "second": "'s'",
        "millisecond": "'ms'",
        "'a'": "'a'",
        "'mo'": "'mo'",
        "'wk'": "'wk'",
        "'d'": "'d'",
        "'h'": "'h'",
        "'min'": "'min'",
        "'s'": "'s'",
        "'ms'": "'ms'",
    }

    """
    A map of the UCUM units that must be paired with integer values when doing arithmetic.
    """
    integerUnits = {
        "'a'": True,
        "'mo'": True,
        "'wk'": True,
        "'d'": True,
        "'h'": True,
        "'min'": True,
    }

    def __init__(self, value, unit):
        super.__init__(value, unit)
        self.asStr = value + " " + unit
        self.value = value
        self.unit = unit

    def toString(self):
        return self.asStr


class FP_TimeBase(FP_Type):
    datetime_multipliers = [
        {"key": "year", "value": (365 * 12 * 24 * 60 * 60)},
        {"key": "month", "value": (12 * 24 * 60 * 60)},
        {"key": "day", "value": (24 * 60 * 60)},
        {"key": "hour", "value": (60 * 60)},
        {"key": "minute", "value": 60},
        {"key": "second", "value": 1},
        {"key": "tz", "value": (60 * 60)}
    ]

    def _extractAsMatchList(self, matchDate, matchGroupsIndices):
        dateTimeListResult = []
        if matchDate and matchGroupsIndices:
            timeMatchGroups = [group for group in matchDate.groups() if group]
            for matchGroupsIndex in matchGroupsIndices:
                if len(timeMatchGroups) >= matchGroupsIndex['index']:
                    dateTimeListResult.append(timeMatchGroups[matchGroupsIndex['index']])
        return dateTimeListResult

    def _getMatchAsList(self):
        raise NotImplementedError()

    def _getDateTimeInt(self):
        raise NotImplementedError()

    def equals(self, otherDateTime):
        """
            From the 2020 August:
            For DateTime and Time equality, the comparison is performed by
            considering each precision in order, beginning with years (or hours for
            time values), and respecting timezone offsets. If the values are the
            same, comparison proceeds to the next precision; if the values are
            different, the comparison stops and the result is false. If one input has
            a value for the precision and the other does not, the comparison stops
            and the result is empty ({ }); if neither input has a value for the
            precision, or the last precision has been reached, the comparison stops
            and the result is true.
            Note:  Per the spec above
        :return:
            2012-01 = 2012 returns empty
            2012-01 = 2011 returns false
            2012-01 ~ 2012 returns false
        """
        if type(otherDateTime) != type(self):
            return False

        thisDateTimeList = self._getMatchAsList()
        otherDateTimeList = otherDateTime._getMatchAsList()

        if self._precision == otherDateTime._precision:
            return self._getDateTimeInt() == otherDateTime._getDateTimeInt()

        morePrecDateTimeList = thisDateTimeList if self._precision >= otherDateTime._precision else otherDateTimeList
        lessPrecDateTimeList = otherDateTimeList if self._precision >= otherDateTime._precision else thisDateTimeList

        for lessPrecDateTimeElementIndex, lessPrecDateTimeElement in enumerate(lessPrecDateTimeList):
            if lessPrecDateTimeElement != morePrecDateTimeList[lessPrecDateTimeElementIndex]:
                return False

        return None

    def compare(self, otherDateTime):
        if type(otherDateTime) != type(self):
            raise TypeError

        thisDateTimeList = self._getMatchAsList()
        otherDateTimeList = otherDateTime._getMatchAsList()

        if self._precision != otherDateTime._precision:
            for precision in range(self._precision):
                if len(otherDateTimeList) >= precision:
                    if thisDateTimeList[precision] > otherDateTimeList[precision]:
                        return 1
                return -1

        thisDateTimeInt = self._getDateTimeInt()
        otherDateTimeInt = otherDateTime._getDateTimeInt()

        if thisDateTimeInt < otherDateTimeInt:
            return -1
        elif thisDateTimeInt == otherDateTimeInt:
            return 0
        return 1


class FP_Time(FP_TimeBase):
    matchGroupsIndices = [
        {"key": "hour", "index": 0},
        {"key": "minute", "index": 1},
        {"key": "second", "index": 2}
    ]

    def __new__(cls, dateStr):
        if not isinstance(dateStr, str):
            return None

        if not re.match(timeRE, dateStr):
            return None

        return super(FP_Time, cls).__new__(cls)

    def __init__(self, timeStr):
        self.asStr = timeStr if isinstance(timeStr, str) else None
        self._timeMatchData = re.match(timeRE, self.asStr)
        self._timeMatchStr = None
        self._timeAsList = []
        self._precision = 0
        self._pyTimeObject = None

        if self._timeMatchData:
            self._timeMatchStr = self._timeMatchData.group(0)
            self._timeAsList = self._extractAsMatchList(self._timeMatchData, self.matchGroupsIndices)
            self._precision = len(self._timeAsList)
            self._pyTimeObject = datetime.datetime.strptime(self.asStr, '%H:%M:%S').time()

    def getTimeMatchStr(self):
        return self._timeMatchStr

    def _getMatchAsList(self):
        return self._timeAsList

    def _getDateTimeInt(self):
        """
        :return: If self.timeMatchData returns DateTime object converted to seconds int, else returns None
        """
        if self._pyTimeObject:
            return datetime.timedelta(
                hours=self._pyTimeObject.hour,
                minutes=self._pyTimeObject.minute,
                seconds=self._pyTimeObject.second
            ).total_seconds()
        return None


class FP_DateTime(FP_TimeBase):
    matchGroupsIndices = [
        {"key": "year", "index": 0},
        {"key": "month", "index": 4},
        {"key": "day", "index": 6},
        {"key": "hour", "index": 8},
        {"key": "minute", "index": 9},
        {"key": "second", "index": 10},
        {"key": "timezone", "index": 12},
    ]
    minPrecision = 3

    def __new__(cls, dateStr):
        if not isinstance(dateStr, str):
            return None

        if not re.match(dateTimeRE, dateStr):
            return None

        return super(FP_DateTime, cls).__new__(cls)

    def __init__(self, dateStr):
        self.asStr = dateStr if isinstance(dateStr, str) else None
        self._dateTimeMatchData = re.match(dateTimeRE, self.asStr) if isinstance(self.asStr, str) else None
        self._dateTimeMatchStr = None
        self._dateTimeAsList = []
        self._precision = 0

        if self._dateTimeMatchData:
            self._dateTimeMatchStr = self._dateTimeMatchData.group(0)
            self._dateTimeAsList = self._extractAsMatchList(self._dateTimeMatchData, self.matchGroupsIndices)
            self._precision = len(self._dateTimeAsList)

    def getDateTimeMatchStr(self):
        return self._dateTimeMatchStr

    def _getMatchAsList(self):
        return self._dateTimeAsList

    def _getDateTimeObject(self):
        if self._dateTimeMatchData:
            return datetime.datetime.fromisoformat(self.asStr)
        return None

    def _getDateTimeInt(self):
        """
        :return: If self.timeMatchData returns DateTime object converted to seconds int, else returns None
        """
        if not self._dateTimeMatchData:
            return None

        if self._precision >= FP_DateTime.minPrecision:
            dateTimeObject = self._getDateTimeObject()
            return dateTimeObject.timestamp()

        integer_result = 0
        for prec in range(self._precision):
            integer_result += int(self._dateTimeAsList[prec]) * self.datetime_multipliers[prec]['value']

        return integer_result


class ResourceNode:
    """
    *  Constructs a instance for the given node ("data") of a resource.  If the
    *  data is the top-level node of a resouce, the path and type parameters will
    *  be ignored in favor of the resource's resourceType field.
    * @param data the node's data or value (which might be an object with
    *  sub-nodes, an array, or FHIR data type)
    * @param path the node's path in the resource (e.g. Patient.name).  If the
    *  data's type can be determined from data, that will take precedence over
    *  this parameter.
    """

    def __init__(self, data, path):
        """
    If data is a resource (maybe a contained resource) reset the path
    information to the resource type.
    """
        if type(data) == dict and "resourceType" in data:
            path = data["resourceType"]

        self.path = path
        self.data = data

    def __eq__(self, value):
        if isinstance(value, ResourceNode):
            return self.data == value.data
        return self.data == value

    def __hash__(self):
        return self.data

    def toJSON(self):
        return json.dumps(self.data)

    @staticmethod
    def create_node(data, path=None):
        if isinstance(data, ResourceNode):
            return data
        return ResourceNode(data, path)
