import json
import re

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


# TODO
class FP_TimeBase(FP_Type):
    # Multipliers need to convert DateTime object to seconds int
    datetime_multipliers = [
        {"key": "year", "value": (365 * 12 * 24 * 60 * 60)},
        {"key": "month", "value": (12 * 24 * 60 * 60)},
        {"key": "day", "value": (24 * 60 * 60)},
        {"key": "hour", "value": (60 * 60)},
        {"key": "minute", "value": 60},
        {"key": "second", "value": 1},
        {"key": "tz", "value": (60 * 60)}
    ]

    def __init__(self, timeStr):
        self.asStr = timeStr if isinstance(timeStr, str) else None
        self.timeMatchData = None

    def getMatchStr(self):
        if self.timeMatchData:
            return self.timeMatchData.group(0)
        return None

    def getMatchGroups(self):
        if self.timeMatchData:
            return [group for group in self.timeMatchData.groups() if group]
        return []

    def getPrecision(self):
        if self.timeMatchData:
            result_prec = 0
            matchGroups = self.getMatchGroups()
            if type(self) == FP_DateTime:
                matchGroupsIndices = FP_DateTime.matchGroupsIndices
                for matchGroupsIndex in matchGroupsIndices:
                    if len(matchGroups) >= matchGroupsIndex['index']:
                        result_prec += 1
                return result_prec
            elif type(self) == FP_Time:
                return 3
            return result_prec
        return 0

    def _getMatchData(self, regEx):
        if not self.timeMatchData:
            if self.asStr:
                self.timeMatchData = re.match(regEx, self.asStr)
        return self.timeMatchData

    def getDateTimeInt(self, maxPrecision=6):
        """
        :return: If self.timeMatchData returns DateTime object converted to seconds int, else returns None
        """
        if self.timeMatchData:
            integer_result = 0
            matchGroups = self.getMatchGroups()
            if type(self) == FP_DateTime:
                matchGroupsIndices = FP_DateTime.matchGroupsIndices
                for prec in range(maxPrecision):
                    if len(matchGroups) >= matchGroupsIndices[prec]['index']:
                        integer_result += int(matchGroups[matchGroupsIndices[prec]['index']]) * \
                                          self.datetime_multipliers[prec]['value']

            elif type(self) == FP_Time:
                matchGroupsIndices = FP_Time.matchGroupsIndices
                integer_result += int(matchGroups[matchGroupsIndices[0]['index']]) * (60 * 60)
                integer_result += int(matchGroups[matchGroupsIndices[1]['index']]) * 60
                integer_result += int(matchGroups[matchGroupsIndices[2]['index']])
            return integer_result
        return None

    def equals(self, otherDateTime=None):
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
        if type(otherDateTime) != type(self) or (not self.timeMatchData or not otherDateTime.timeMatchData):
            return False
        else:
            thisMatchGroups = self.getMatchGroups()
            thisPrec = self.getPrecision()
            otherMatchGroups = otherDateTime.getMatchGroups()
            otherPrec = otherDateTime.getPrecision()
            if thisPrec == otherPrec:
                return self.getDateTimeInt() == otherDateTime.getDateTimeInt()
            else:
                morePrecMatchGroups = thisMatchGroups if thisPrec >= otherPrec else otherMatchGroups
                lessPrecMatchGroups = otherMatchGroups if thisPrec >= otherPrec else thisMatchGroups
                matchGroupsIndices = otherDateTime.__class__.matchGroupsIndices
                for matchGroupsIndex in matchGroupsIndices:
                    if len(morePrecMatchGroups) >= matchGroupsIndex['index'] and len(lessPrecMatchGroups) >= matchGroupsIndex['index']:
                        if morePrecMatchGroups[matchGroupsIndex['index']] != lessPrecMatchGroups[matchGroupsIndex['index']]:
                            return False
                return None

    def compare(self, otherDateTime=None):
        if type(otherDateTime) != type(self):
            raise TypeError

        thisPrec = self.getPrecision()
        otherPrec = otherDateTime.getPrecision()

        if thisPrec != otherPrec:
            lessPrec = thisPrec if thisPrec < otherPrec else otherPrec
        else:
            lessPrec = thisPrec

        thisDateTimeInt = self.getDateTimeInt(lessPrec)
        otherDateTimeInt = otherDateTime.getDateTimeInt(lessPrec)
        return -1 if thisDateTimeInt < otherDateTimeInt else 0 if thisDateTimeInt == otherDateTimeInt else 1

    @staticmethod
    def check_string(value):
        """
        Tests str to see if it is convertible to a DateTime or Time.
        * @return If str is convertible to a DateTime or Time, returns an FP_DateTime
            or FP_Time otherwise returns None
        """
        d = FP_DateTime(value)
        if not d._getMatchData(dateTimeRE):
            d = FP_Time(value)
            if not d._getMatchData(timeRE):
                return None
        return d


# TODO
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

    def __init__(self, timeStr):
        super(FP_DateTime, self).__init__(timeStr)
        self.timeMatchData = self._getMatchData(dateTimeRE)

    def _getMatchData(self, regEx):
        return super(FP_DateTime, self)._getMatchData(regEx)

    @staticmethod
    def check_string(value):
        """
        Tests str to see if it is convertible to a DateTime.
        * @return If str is convertible to a DateTime, returns an FP_DateTime otherwise returns None
        """
        d = FP_DateTime(value)
        if not d._getMatchData(dateTimeRE):
            return None
        return d


# TODO
class FP_Time(FP_TimeBase):

    matchGroupsIndices = [
        {"key": "hour", "index": 0},
        {"key": "minute", "index": 1},
        {"key": "second", "index": 2}
    ]

    def __init__(self, timeStr):
        super(FP_Time, self).__init__(timeStr)
        self.timeMatchData = self._getMatchData(timeRE)

    def _getMatchData(self, regEx):
        return super(FP_Time, self)._getMatchData(regEx)

    @staticmethod
    def check_string(value):
        """
        Tests str to see if it is convertible to a DateTime.
        * @return If str is convertible to a DateTime, returns an FP_Time otherwise returns None
        """
        d = FP_Time(value)
        if not d._getMatchData(timeRE):
            return None
        return d


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
