import datetime


class Constants:
    """
    These are values that should not change during an evaluation of a FHIRPath
    expression (e.g. the return value of today(), per the spec.)  They are
    constant during at least one evaluation.
    """

    nowDate = datetime.datetime.now()
    today = None
    now = None
    timeOfDay = None
    localTimezoneOffset = None

    @classmethod
    def reset(cls):
        cls.nowDate = datetime.datetime.now()
        cls.today = None
        cls.now = None
        cls.timeOfDay = None
        cls.localTimezoneOffset = None

constants = Constants()
