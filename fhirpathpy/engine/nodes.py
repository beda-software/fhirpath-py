import json
import re

dateFormat = '([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])'
dateRe = '%s)?)?' % dateFormat

timeRE = '([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?'

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

    def __init__(self, timeStr):
        self.asStr = timeStr
        self.timeMatchData = None

    def _getMatchData(self, regEx):
        if not self.timeMatchData:
            self.timeMatchData = re.match(regEx, self.asStr).group(0)
        return self.timeMatchData


# TODO
class FP_DateTime(FP_TimeBase):

    def __init__(self, timeStr):
        super(FP_DateTime, self).__init__(timeStr)
        self.timeMatchData = self._getMatchData()

    def _getMatchData(self, regEx=dateTimeRE):
        return super(FP_DateTime, self)._getMatchData(regEx)

    @staticmethod
    def check_string(value):
        """
        Tests str to see if it is convertible to a DateTime.
        * @return If str is convertible to a DateTime, returns an FP_DateTime otherwise returns None
        """
        d = FP_DateTime(value)
        if not d._getMatchData():
            return None
        return d


# TODO
class FP_Date(FP_TimeBase):

    def __init__(self, timeStr):
        super(FP_Date, self).__init__(timeStr)
        self.timeMatchData = self._getMatchData()

    def _getMatchData(self, regEx=dateRe):
        return super(FP_Date, self)._getMatchData(regEx)

    @staticmethod
    def check_string(value):
        """
        Tests str to see if it is convertible to a DateTime.
        * @return If str is convertible to a DateTime, returns an FP_Date otherwise returns None
        """
        d = FP_Date(value)
        if not d._getMatchData():
            return None
        return d


# TODO
class FP_Time(FP_TimeBase):

    def __init__(self, timeStr):
        super(FP_Time, self).__init__(timeStr)
        self.timeMatchData = self._getMatchData()

    def _getMatchData(self, regEx=timeRE):
        return super(FP_Time, self)._getMatchData(regEx)

    @staticmethod
    def check_string(value):
        """
        Tests str to see if it is convertible to a DateTime.
        * @return If str is convertible to a DateTime, returns an FP_Time otherwise returns None
        """
        d = FP_Time(value)
        if not d._getMatchData():
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
