import datetime
from datetime import timezone
from decimal import Decimal
import json
import re
import time

dateFormat = "([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])"
timeRE = r"^T?([01][0-9]|2[0-3]):([0-5][0-9])(?::([0-5][0-9]|60))?(\.[0-9]+)?([-+][0-2][0-9]:?[0-5][0-9])?$"
dateTimeRE = "%s(T%s(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))?)?)?" % (dateFormat, timeRE)


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

    _years_and_months = [
        "'a'",
        "year",
        "years",
        "'mo'",
        "month",
        "months",
    ]

    _weeks_days_and_time = [
        "'wk'",
        "week",
        "weeks",
        "'d'",
        "day",
        "days",
        "'h'",
        "hour",
        "hours",
        "'min'",
        "minute",
        "minutes",
        "'s'",
        "second",
        "seconds",
        "'ms'",
        "millisecond",
        "milliseconds",
    ]

    _year_month_conversion_factor = {"'a'": 12, "'mo'": 1}
    _m_cm_mm_conversion_factor = {"'m'": 1.0, "'cm'": 0.01, "'mm'": 0.001}

    datetime_multipliers = {
        **{key: Decimal("604800") for key in ["'wk'", "week", "weeks"]},
        **{key: Decimal("86400") for key in ["'d'", "day", "days"]},
        **{key: Decimal("3600") for key in ["'h'", "hour", "hours"]},
        **{key: Decimal("60") for key in ["'min'", "minute", "minutes"]},
        **{key: Decimal("1") for key in ["'s'", "second", "seconds"]},
        **{key: Decimal("0.001") for key in ["'ms'", "millisecond", "milliseconds"]},
    }

    def __init__(self, value, unit):
        super().__init__()
        self.asStr = f"{value} {unit}"
        self.value = value
        self.unit = unit

    def __str__(self):
        return self.asStr

    def __repr__(self):
        return f"{type(self)}<{self.asStr}>"

    def __hash__(self):
        if self.unit in self._years_and_months:
            value_in_months = self.value
            if self.unit in ["'a'", "year", "years"]:
                value_in_months *= 12
            return hash(("months", value_in_months))
        elif self.unit in self._weeks_days_and_time:
            value_in_seconds = self.value * self.datetime_multipliers[self.unit]
            return hash(("seconds", value_in_seconds))
        else:
            return hash((self.value, self.unit))

    def __eq__(self, other):
        if isinstance(other, FP_Quantity):
            if self.unit in self._years_and_months and other.unit in self._years_and_months:
                return self._compare_years_and_months(other)
            elif self.unit in self._weeks_days_and_time and other.unit in self._weeks_days_and_time:
                self_value_in_seconds = self.value * self.datetime_multipliers[self.unit]
                other_value_in_seconds = other.value * self.datetime_multipliers[other.unit]
                return self_value_in_seconds == other_value_in_seconds
            else:
                return self.value == other.value and self.unit == other.unit
        else:
            return super().__eq__(other)

    def deep_equal(self, other):
        if isinstance(other, FP_Quantity):
            if self.unit in self._years_and_months and other.unit in self._years_and_months:
                return self._compare_years_and_months(other, year_units=["'a'", "year", "years"])
            else:
                return self.__eq__(other)
        else:
            return super().__eq__(other)

    def conv_unit_to(fromUnit, value, toUnit):
        ## 1 Year <-> 12 Months
        from_year_month_magnitude = FP_Quantity._year_month_conversion_factor.get(fromUnit)
        to_year_month_magnitude = FP_Quantity._year_month_conversion_factor.get(toUnit)

        if from_year_month_magnitude and to_year_month_magnitude:
            return FP_Quantity(from_year_month_magnitude * value / to_year_month_magnitude, toUnit)

        elif (
            fromUnit in FP_Quantity._weeks_days_and_time
            and toUnit in FP_Quantity._weeks_days_and_time
        ):
            value_in_seconds = value * FP_Quantity.datetime_multipliers.get(fromUnit)
            new_value = value_in_seconds / FP_Quantity.datetime_multipliers.get(toUnit)
            return FP_Quantity(new_value, toUnit)

        from_m_cm_mm_magnitude = FP_Quantity._m_cm_mm_conversion_factor.get(fromUnit)
        to_m_cm_mm_magnitude = FP_Quantity._m_cm_mm_conversion_factor.get(toUnit)
        if from_m_cm_mm_magnitude and to_m_cm_mm_magnitude:
            if (
                fromUnit in FP_Quantity._m_cm_mm_conversion_factor
                or toUnit in FP_Quantity._m_cm_mm_conversion_factor
            ):
                from_magnitude, to_magnitude = Decimal(from_m_cm_mm_magnitude), Decimal(
                    to_m_cm_mm_magnitude
                )
            return FP_Quantity(from_magnitude * value / to_magnitude, toUnit)

        return None

    def _compare_years_and_months(self, other, year_units=["year", "years"]):
        self_value_in_months = self.value
        other_value_in_months = other.value

        if self.unit in year_units:
            self_value_in_months *= 12
        if other.unit in year_units:
            other_value_in_months *= 12
        return self_value_in_months == other_value_in_months


class FP_TimeBase(FP_Type):
    datetime_multipliers = [
        {"key": "year", "value": (365 * 12 * 24 * 60 * 60)},
        {"key": "month", "value": (12 * 24 * 60 * 60)},
        {"key": "day", "value": (24 * 60 * 60)},
        {"key": "hour", "value": (60 * 60)},
        {"key": "minute", "value": 60},
        {"key": "second", "value": 1},
        {"key": "tz", "value": (60 * 60)},
    ]

    def _extractAsMatchList(self, matchDate, matchGroupsIndices):
        dateTimeListResult = []
        if matchDate and matchGroupsIndices:
            timeMatchGroups = [group for group in matchDate.groups() if group]
            for matchGroupsIndex in matchGroupsIndices:
                if len(timeMatchGroups) >= matchGroupsIndex["index"]:
                    dateTimeListResult.append(timeMatchGroups[matchGroupsIndex["index"]])
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

        morePrecDateTimeList = (
            thisDateTimeList if self._precision >= otherDateTime._precision else otherDateTimeList
        )
        lessPrecDateTimeList = (
            otherDateTimeList if self._precision >= otherDateTime._precision else thisDateTimeList
        )

        for lessPrecDateTimeElementIndex, lessPrecDateTimeElement in enumerate(
            lessPrecDateTimeList
        ):
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
        {"key": "second", "index": 2},
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
            self._timeAsList = self._extractAsMatchList(
                self._timeMatchData, self.matchGroupsIndices
            )
            self._precision = len(self._timeAsList)
            formats = [
                "T%H:%M:%S%z",
                "T%H:%M:%S.%f%z",
                "T%H:%M:%S",
                "T%H:%M:%S.%f",
                "T%H:%M%z",
                "%H:%M:%S%z",
                "%H:%M:%S.%f%z",
                "%H:%M:%S",
                "%H:%M:%S.%f",
                "%H:%M%z",
            ]

            for fmt in formats:
                try:
                    parsed_datetime = datetime.datetime.strptime(self.asStr, fmt)
                    if parsed_datetime.tzinfo:
                        parsed_datetime = parsed_datetime.astimezone(timezone.utc)
                    self._pyTimeObject = parsed_datetime.time()
                    break
                except ValueError:
                    continue

    def __str__(self):
        if self._pyTimeObject:
            time_str = self._pyTimeObject.isoformat()
            if "." in time_str:
                time_str = time_str[: time_str.index(".") + 4]
            return time_str
        return self.asStr

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
                seconds=self._pyTimeObject.second,
                microseconds=self._pyTimeObject.microsecond,
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
        self._dateTimeMatchData = (
            re.match(dateTimeRE, self.asStr) if isinstance(self.asStr, str) else None
        )
        self._dateTimeMatchStr = None
        self._dateTimeAsList = []
        self._precision = 0

        if self._dateTimeMatchData:
            self._dateTimeMatchStr = self._dateTimeMatchData.group(0)
            self._dateTimeAsList = self._extractAsMatchList(
                self._dateTimeMatchData, self.matchGroupsIndices
            )
            self._precision = len(self._dateTimeAsList)

    def __str__(self):
        if self.asStr and len(self.asStr) <= 4:
            return self.asStr
        if self._getDateTimeObject():
            iso_str = self._getDateTimeObject().isoformat()
            if "." in iso_str:
                iso_str = iso_str[: iso_str.index(".") + 4] + iso_str[iso_str.index(".") + 7 :]
            return iso_str
        return self.asStr

    def getDateTimeMatchStr(self):
        return self._dateTimeMatchStr

    def _getMatchAsList(self):
        return self._dateTimeAsList

    def _getDateTimeObject(self):
        if self._dateTimeMatchData:
            if "Z" in self.asStr:
                date_str = self.asStr.replace("Z", "+00:00")
            else:
                date_str = self.asStr
            return datetime.datetime.fromisoformat(date_str)
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
            integer_result += (
                int(self._dateTimeAsList[prec]) * self.datetime_multipliers[prec]["value"]
            )

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
        data_hash = hash(json.dumps(self.data, sort_keys=True))
        path_hash = hash(self.path)
        return hash((data_hash, path_hash))

    def toJSON(self):
        return json.dumps(self.data)

    @staticmethod
    def create_node(data, path=None):
        if isinstance(data, ResourceNode):
            return data
        return ResourceNode(data, path)
