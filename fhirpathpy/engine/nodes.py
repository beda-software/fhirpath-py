import copy
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from dateutil import parser, tz
from decimal import ROUND_HALF_UP, ROUND_UP, Decimal
import math
import json
import re
import time


timeRE = (
    r"^T?([0-9]{2})(?::([0-9]{2}))?(?::([0-9]{2}))?(?:\.([0-9]+))?(Z|(\+|-)[0-9]{2}(:[0-9]{2})?)?$"
)
dateTimeRE = r"^(?P<year>[0-9]{4})(?:-(?P<month>[0-9]{2})(?:-(?P<day>[0-9]{2}))?)?(?:T(?P<hour>[0-9]{2})(?::(?P<minute>[0-9]{2}))?(?::(?P<second>[0-9]{2}))?(?:\.(?P<millisecond>[0-9]+))?(?P<timezone>Z|(\+|-)[0-9]{2}:[0-9]{2})?)?$"


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

    mapUCUMCodeToTimeUnits = {
        "'a'": "year",
        "'mo'": "month",
        "'wk'": "week",
        "'d'": "day",
        "'h'": "hour",
        "'min'": "minute",
        "'s'": "second",
        "'ms'": "millisecond",
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

    _arithmetic_duration_units = {
        "years": "year",
        "months": "month",
        "weeks": "week",
        "days": "day",
        "hours": "hour",
        "minutes": "minute",
        "seconds": "second",
        "milliseconds": "millisecond",
        "year": "year",
        "month": "month",
        "week": "week",
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "second": "second",
        "millisecond": "millisecond",
        "'wk'": "week",
        "'d'": "day",
        "'h'": "hour",
        "'min'": "minute",
        "'s'": "second",
        "'ms'": "millisecond",
    }

    _year_month_conversion_factor = {"'a'": 12, "'mo'": 1}
    _m_cm_mm_conversion_factor = {"'m'": 1.0, "'cm'": 0.01, "'mm'": 0.001}
    _lbs_kg_conversion_factor = {"'kg'": 1.0, "lbs": 0.453592, "'[lb_av]'": 0.453592}
    _g_mg_conversion_factor = {"'g'": 1.0, "'mg'": 0.001}

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
                if self.unit == "'a'" or other.unit == "'a'":
                    return False
                return self._compare_years_and_months(other)
            elif self.unit in self._weeks_days_and_time and other.unit in self._weeks_days_and_time:
                self_value_in_seconds = self.value * self.datetime_multipliers[self.unit]
                other_value_in_seconds = other.value * self.datetime_multipliers[other.unit]
                return self_value_in_seconds == other_value_in_seconds
            else:
                if self.unit != other.unit:
                    converted = FP_Quantity.conv_unit_to(self.unit, self.value, other.unit)
                    if converted is not None:
                        return other.value == converted.value and other.unit == converted.unit

                return self.value == other.value and self.unit == other.unit
        else:
            return super().__eq__(other)

    def deep_equal(self, other):
        if isinstance(other, FP_Quantity):
            if self.unit in self._years_and_months and other.unit in self._years_and_months:
                return self._compare_years_and_months(other, year_units=["'a'", "year", "years"])
            else:
                if self.unit != other.unit:
                    converted = FP_Quantity.conv_unit_to(self.unit, self.value, other.unit)
                    reverse_converted = FP_Quantity.conv_unit_to(
                        converted.unit, converted.value, self.unit
                    )
                    if converted is not None:
                        return (
                            self.value == reverse_converted.value
                            and self.unit == reverse_converted.unit
                        )
                return self.__eq__(other)
        else:
            return super().__eq__(other)

    def conv_unit_to(fromUnit, value, toUnit):
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

        from_lbs_kg_magnitude = FP_Quantity._lbs_kg_conversion_factor.get(fromUnit)
        to_lbs_kg_magnitude = FP_Quantity._lbs_kg_conversion_factor.get(toUnit)
        if from_lbs_kg_magnitude and to_lbs_kg_magnitude:
            converted_value = (Decimal(from_lbs_kg_magnitude) * value) / Decimal(
                to_lbs_kg_magnitude
            )
            rounded_value = converted_value.quantize(Decimal("1."), rounding=ROUND_UP)
            return FP_Quantity(rounded_value, toUnit)

        from_g_mg_magnitude = FP_Quantity._g_mg_conversion_factor.get(fromUnit)
        to_g_mg_magnitude = FP_Quantity._g_mg_conversion_factor.get(toUnit)
        if from_g_mg_magnitude and to_g_mg_magnitude:
            value = Decimal(value) * Decimal(FP_Quantity._g_mg_conversion_factor[fromUnit])
            result = (value / Decimal(FP_Quantity._g_mg_conversion_factor[toUnit])).quantize(
                Decimal("1."), rounding=ROUND_HALF_UP
            )
            return FP_Quantity(result, toUnit)
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

    def _extractAsMatchList(self, matchData, matchGroupsIndices, is_date=True):
        result = []
        for matchGroupIndex in matchGroupsIndices:
            if is_date:
                group = matchData.group(matchGroupIndex["key"])
            else:
                index = matchGroupIndex["index"]
                group = matchData.group(index) if index <= matchData.lastindex else None
            result.append(group if group is not None else None)
        return result

    def _calculatePrecision(self, dt_list):
        return sum(all(x not in i for x in ["+", "-"]) for i in dt_list if i is not None)

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

        thisdt_list = self._getMatchAsList()
        otherdt_list = otherDateTime._getMatchAsList()

        normalized_thisdt_list = self._normalize_datetime(thisdt_list)
        normalized_otherdt_list = self._normalize_datetime(otherdt_list)

        indices_to_remove = [
            i
            for i in range(len(normalized_thisdt_list))
            if normalized_thisdt_list[i] == normalized_otherdt_list[i] == None
        ]

        for i in reversed(indices_to_remove):
            del normalized_thisdt_list[i]
            del normalized_otherdt_list[i]

        normalized_thisdt_precision = self._calculatePrecision(normalized_thisdt_list)
        normalized_otherdt_precision = self._calculatePrecision(normalized_otherdt_list)

        if normalized_thisdt_precision == normalized_otherdt_precision:
            return self._getDateTimeInt() == otherDateTime._getDateTimeInt()

        if normalized_thisdt_precision != normalized_otherdt_precision:
            min_precision = min(normalized_thisdt_precision, normalized_otherdt_precision)
            for i in range(min_precision):
                if normalized_thisdt_list[i] is None or normalized_otherdt_list[i] is None:
                    return None
                if normalized_thisdt_list[i] != normalized_otherdt_list[i]:
                    return False
                tz_thisdt_list = len(thisdt_list) >= 8 and thisdt_list[7] is not None
                tz_otherdt_list = len(otherdt_list) >= 8 and otherdt_list[7] is not None
                if (tz_thisdt_list and not tz_otherdt_list) or (
                    tz_otherdt_list and not tz_thisdt_list
                ):
                    return False

            return None

    def _normalize_datetime(self, dt_list):
        def to_str(number):
            return "0" + str(number) if 0 < number < 10 else str(number)

        if len(dt_list) < 6:
            year, month, day = (None, None, None)
            hour, minute, second = (int(dt_list[i]) if dt_list[i] else None for i in range(3))
            timezone_str = dt_list[4] if len(dt_list) > 4 else None
        else:
            year, month, day = (int(dt_list[i]) if dt_list[i] else None for i in range(3))
            hour, minute, second = (int(dt_list[i]) if dt_list[i] else None for i in range(3, 6))
            timezone_str = dt_list[7] if len(dt_list) > 7 else None

        dt = datetime(year or 2023, month or 1, day or 1, hour or 0, minute or 0, second or 0)
        if timezone_str and timezone_str != "Z":
            tz_hours, tz_minutes = map(int, timezone_str[1:].split(":"))
            tz_delta = timedelta(hours=tz_hours, minutes=tz_minutes)
            dt = dt - tz_delta if timezone_str.startswith("+") else dt + tz_delta

        return [
            to_str(dt.year) if year is not None else None,
            to_str(dt.month) if month is not None else None,
            to_str(dt.day) if day is not None else None,
            to_str(dt.hour) if hour is not None else None,
            to_str(dt.minute) if minute is not None else None,
            to_str(dt.second) if second is not None else None,
        ]

    def compare(self, otherDateTime):
        if type(otherDateTime) != type(self):
            raise TypeError

        thisDateTimeList = self._getMatchAsList()
        otherDateTimeList = otherDateTime._getMatchAsList()

        normalized_thisdt_list = self._normalize_datetime(thisDateTimeList)
        normalized_otherdt_list = self._normalize_datetime(otherDateTimeList)
        indices_to_remove = [
            i
            for i in range(len(normalized_thisdt_list))
            if normalized_thisdt_list[i] == normalized_otherdt_list[i] == None
        ]
        for i in reversed(indices_to_remove):
            del normalized_thisdt_list[i]
            del normalized_otherdt_list[i]

        normalized_thisdt_precision = self._calculatePrecision(normalized_thisdt_list)
        normalized_otherdt_precision = self._calculatePrecision(normalized_otherdt_list)

        if normalized_thisdt_precision != normalized_otherdt_precision:
            min_precision = min(normalized_thisdt_precision, normalized_otherdt_precision)
            for i in range(min_precision):
                if normalized_thisdt_list[i] is None or normalized_otherdt_list[i] is None:
                    return -1
                if normalized_thisdt_list[i] > normalized_otherdt_list[i]:
                    return 1
                if normalized_thisdt_list[i] < normalized_otherdt_list[i]:
                    return -1
            return None

        thisDateTimeInt = self._getDateTimeInt()
        otherDateTimeInt = otherDateTime._getDateTimeInt()

        if thisDateTimeInt < otherDateTimeInt:
            return -1
        elif thisDateTimeInt == otherDateTimeInt:
            return 0
        return 1

    def plus(self, time_quantity):
        value = int(time_quantity.value)
        time_unit = FP_Quantity._arithmetic_duration_units.get(time_quantity.unit)
        if time_unit is None:
            valid_units = ", ".join(FP_Quantity._arithmetic_duration_units.keys())
            raise ValueError(
                f"For date/time arithmetic, the unit of the quantity must be one of the following time-based units: {valid_units}"
            )
        dt_list = self._getMatchAsList()
        if isinstance(self, FP_DateTime):
            precision = self._calculatePrecision(dt_list)
            date_obj = self._convertDatetime(dt_list)
            if time_unit == "year":
                result = date_obj + relativedelta(years=value)
            if time_unit == "month":
                result = date_obj + relativedelta(months=value)
            if time_unit in ["day", "week"]:
                if time_unit == "week":
                    value *= 7
                if precision == 1:
                    years = math.floor(value / 365) if value >= 0 else math.ceil(value / 365)
                    result = date_obj + relativedelta(years=years)
                elif precision == 2:
                    months = math.floor(value / 30) if value >= 0 else math.ceil(value / 30)
                    result = date_obj + relativedelta(months=months)
                else:
                    result = date_obj + relativedelta(days=value)
            if time_unit in ["hour"]:
                if precision == 2:
                    months = (
                        math.floor(value / (24 * 30))
                        if value >= 0
                        else math.ceil(value / (24 * 30))
                    )
                    result = date_obj + relativedelta(months=months)
                if precision == 3:
                    days = math.floor(value / 24) if value >= 0 else math.ceil(value / 24)
                    result = date_obj + relativedelta(days=days)
            if time_unit in ["minute", "second", "millisecond"]:
                if precision == 4:
                    if time_unit == "minute":
                        hours = math.floor(value / 60) if value >= 0 else math.ceil(value / 60)
                        result = date_obj + relativedelta(hours=hours)
                    if time_unit == "second":
                        hours = (
                            math.floor(value / (60 * 60))
                            if value >= 0
                            else math.ceil(value / (60 * 60))
                        )
                        result = date_obj + relativedelta(hours=hours)
                    if time_unit == "millisecond":
                        hours = (
                            math.floor(value / (60 * 60 * 1000))
                            if value >= 0
                            else math.ceil(value / (60 * 60 * 1000))
                        )
                        result = date_obj + relativedelta(hours=hours)
                if precision == 5:
                    if time_unit == "minute":
                        minutes = math.floor(value) if value >= 0 else math.ceil(value)
                        result = date_obj + relativedelta(minutes=minutes)
                    if time_unit == "second":
                        minutes = math.floor(value / 60) if value >= 0 else math.ceil(value / 60)
                        result = date_obj + relativedelta(minutes=minutes)
                    if time_unit == "millisecond":
                        minutes = (
                            math.floor(value / (60 * 1000))
                            if value >= 0
                            else math.ceil(value / (60 * 1000))
                        )
                        result = date_obj + relativedelta(minutes=minutes)
            return self._extractDateByPrecision(result, precision)
        if isinstance(self, FP_Time):
            precision = self._calculateTimePrecision(dt_list)
            date_obj = self._convertTime(dt_list)
            if precision == 2:
                if time_unit == "hour":
                    result = date_obj + relativedelta(minutes=value * 60)
                if time_unit == "minute":
                    result = date_obj + relativedelta(minutes=value)
                if time_unit == "second":
                    minutes = math.floor(value / 60) if value >= 0 else math.ceil(value / 60)
                    result = date_obj + relativedelta(minutes=minutes)
                if time_unit == "millisecond":
                    minutes = (
                        math.floor(value / (60 * 1000))
                        if value >= 0
                        else math.ceil(value / (60 * 1000))
                    )
                    result = date_obj + relativedelta(minutes=minutes)
            if precision in [3, 4]:
                if time_unit == "hour":
                    result = date_obj + relativedelta(minutes=value * 60)
                if time_unit == "minute":
                    result = date_obj + relativedelta(minutes=value)
                if time_unit == "second":
                    milliseconds = float(str(time_quantity).split()[0]) * 1000
                    result = date_obj + relativedelta(microseconds=milliseconds * 1000)
                if time_unit == "millisecond":
                    result = date_obj + relativedelta(microseconds=value * 1000)
            return (
                self._extractTimeByPrecision(result, precision if precision < 3 else 4) + dt_list[4]
            )

    @staticmethod
    def check_string(cls, str_val):
        val = cls(str_val)
        return val

    @staticmethod
    def get_match_data(str_val):
        match = re.match(dateTimeRE, str_val)
        if match:
            return FP_DateTime(str_val)
        match = re.match(timeRE, str_val)
        if match:
            return FP_Time(str_val)
        return None


class FP_Time(FP_TimeBase):
    matchGroupsIndices = [
        {"key": "hour", "index": 1},
        {"key": "minute", "index": 2},
        {"key": "second", "index": 3},
        {"key": "millisecond", "index": 4},
        {"key": "timezone", "index": 5},
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
                self._timeMatchData, self.matchGroupsIndices, is_date=False
            )
            self._precision = self._calculatePrecision(self._timeAsList)
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
                "%H:%M",
                "%H%z",
            ]

            for fmt in formats:
                try:
                    parsed_datetime = datetime.strptime(self.asStr, fmt)
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

    def __eq__(self, other):
        if isinstance(other, str):
            return self.getTimeMatchStr()

    def getTimeMatchStr(self):
        return self._timeMatchStr

    def _getMatchAsList(self):
        return self._timeAsList

    def _getDateTimeInt(self):
        """
        :return: If self.timeMatchData returns DateTime object converted to seconds int, else returns None
        """
        if self._pyTimeObject:
            return timedelta(
                hours=self._pyTimeObject.hour,
                minutes=self._pyTimeObject.minute,
                seconds=self._pyTimeObject.second,
                microseconds=self._pyTimeObject.microsecond,
            ).total_seconds()
        return None

    def _extractTimeByPrecision(self, date_obj, precision):
        format = {1: "T%H", 2: "T%H:%M", 3: "T%H:%M:%S", 4: "T%H:%M:%S.%f"}
        return date_obj.strftime(format.get(precision)) if precision in format else None

    def _calculateTimePrecision(self, dt_list):
        return sum(1 for i in dt_list[0:4] if i is not None)

    def _convertTime(self, time_list):
        hour = time_list[0] if time_list[0] is not None else 00
        minute = time_list[1] if time_list[1] is not None else 00
        second = time_list[2] if time_list[2] is not None else 00
        millisecond = time_list[3] if time_list[3] is not None else 000
        return datetime.strptime(f"{hour}:{minute}:{second}.{millisecond}", "%H:%M:%S.%f")


class FP_DateTime(FP_TimeBase):
    matchGroupsIndices = [
        {"key": "year", "index": 0},
        {"key": "month", "index": 4},
        {"key": "day", "index": 6},
        {"key": "hour", "index": 8},
        {"key": "minute", "index": 9},
        {"key": "second", "index": 10},
        {"key": "millisecond", "index": 11},
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
            self._precision = self._calculatePrecision(self._dateTimeAsList)

    def __str__(self):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", self.asStr):
            return self.asStr
        if self.asStr and len(self.asStr) <= 4:
            return self.asStr
        if self._getDateTimeObject():
            iso_str = self._getDateTimeObject().isoformat()
            if "." in iso_str:
                iso_str = iso_str[: iso_str.index(".") + 4] + iso_str[iso_str.index(".") + 7 :]
            return iso_str
        return self.asStr

    def __eq__(self, other):
        if isinstance(other, str):
            return self.getDateTimeMatchStr()

    def __deepcopy__(self, memo):
        return type(self)(copy.deepcopy(self.asStr, memo))

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
            return parser.parse(date_str)
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

    def _extractDateByPrecision(self, date_obj: datetime, precision):
        if date_obj.tzinfo is None or date_obj.tzinfo.utcoffset(date_obj) is None:
            date_obj = date_obj.replace(tzinfo=tz.tzutc())
        format = {
            1: "%Y",
            2: "%Y-%m",
            3: "%Y-%m-%d",
            4: "%Y-%m-%dT%H",
            5: "%Y-%m-%dT%H:%M",
            6: "%Y-%m-%dT%H:%M:%S",
            7: "%Y-%m-%dT%H:%M:%S",
        }
        formatted_date = date_obj.strftime(format.get(precision, ""))
        if precision == 7:
            milliseconds = date_obj.strftime("%f")[:3]
            tz_offset = date_obj.strftime("%z")
            tz_formatted = tz_offset[:3] + ":" + tz_offset[3:]
            formatted_date = f"{formatted_date}.{milliseconds}{tz_formatted}"
        return formatted_date

    def _convertDatetime(self, date_list):
        n_date_list = self._normalize_datetime(date_list)
        year = n_date_list[0] if n_date_list[0] is not None else "0"
        month = n_date_list[1] if n_date_list[1] is not None else "01"
        day = n_date_list[2] if n_date_list[2] is not None else "01"
        hour = n_date_list[3] if n_date_list[3] is not None else "00"
        minute = n_date_list[4] if n_date_list[4] is not None else "00"
        second = n_date_list[5] if n_date_list[5] is not None else "00"
        millisecond = date_list[6] if date_list[6] is not None else "000"
        date_string = f"{year}-{month}-{day} {hour}:{minute}:{second}.{millisecond}"
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")


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
    * @param _data additional data stored in a property named with "_" prepended.
    """

    def __init__(self, data, path, _data=None):
        """
        If data is a resource (maybe a contained resource) reset the path
        information to the resource type.
        """
        if isinstance(data, dict) and "resourceType" in data:
            path = data["resourceType"]

        self.path = path
        self.data = data
        self._data = _data

    def __eq__(self, value):
        if isinstance(value, ResourceNode):
            return self.data == value.data
        return self.data == value

    def __hash__(self):
        data_hash = hash(json.dumps(self.data, sort_keys=True))
        path_hash = hash(self.path)
        return hash((data_hash, path_hash))

    def get_type_info(self):
        namespace = TypeInfo.FHIR

        if self.path is None:
            return None

        match = re.match(r"^System\.(.*)$", self.path)
        if match:
            return TypeInfo(namespace=TypeInfo.System, name=match.group(1))
        elif "." not in self.path:
            return TypeInfo(namespace=namespace, name=self.path)

        if not TypeInfo.model:
            return TypeInfo.create_by_value_in_namespace(namespace=namespace, value=self.data)

        return TypeInfo(namespace=namespace, name="BackboneElement")

    def toJSON(self):
        return json.dumps(self.data)

    @staticmethod
    def create_node(data, path=None, _data=None):
        if isinstance(data, ResourceNode):
            return data
        return ResourceNode(data, path, _data)

    def convert_data(self):
        data = self.data
        cls = TypeInfo.type_to_class_with_check_string.get(self.path)
        if cls:
            data = FP_TimeBase.check_string(cls, data) or data
        if isinstance(data, dict) and data["system"] == "http://unitsofmeasure.org":
            data = FP_Quantity(
                data["value"],
                FP_Quantity.timeUnitsToUCUM.get(data["code"], "'" + data["code"] + "'"),
            )
        return data


class TypeInfo:
    model = None
    System = "System"
    FHIR = "FHIR"

    type_to_class_with_check_string = {
        "date": FP_DateTime,
        "dateTime": FP_DateTime,
        "time": FP_Time,
    }

    def __init__(self, name, namespace):
        self.name = name
        self.namespace = namespace

    @staticmethod
    def is_type(type_name, super_type):
        while type_name:
            if type_name == super_type:
                return True

            # TODO: Double check it
            type_name = TypeInfo.model.get("type2Parent").get(type_name) or TypeInfo.model.get(
                "path2Type"
            ).get(type_name)

        return False

    def is_(self, other):
        if isinstance(other, TypeInfo) and (
            not self.namespace or not other.namespace or self.namespace == other.namespace
        ):
            if TypeInfo.model and (not self.namespace or self.namespace == TypeInfo.FHIR):
                return TypeInfo.is_type(self.name, other.name)
            else:
                return self.name == other.name
        return False

    @staticmethod
    def create_by_value_in_namespace(namespace, value):
        name = type(value).__name__

        if isinstance(value, int) and not isinstance(value, bool):
            name = "integer"
        elif isinstance(value, float) or isinstance(value, Decimal):
            name = "decimal"
        elif isinstance(value, FP_DateTime):
            name = "dateTime"
        elif isinstance(value, FP_Time):
            name = "time"
        elif isinstance(value, FP_Quantity):
            name = "Quantity"
        elif isinstance(value, str):
            name = "string"
        elif isinstance(value, dict):
            name = "object"

        if name == "bool":
            name = "boolean"

        if namespace == TypeInfo.System:
            if name == "dateTime":
                name = "DateTime"
            else:
                name = name.capitalize()

        return TypeInfo(name, namespace)

    @staticmethod
    def from_value(value):
        if isinstance(value, ResourceNode):
            return value.get_type_info()
        else:
            return TypeInfo.create_by_value_in_namespace(TypeInfo.System, value)
