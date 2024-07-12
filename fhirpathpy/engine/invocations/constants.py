from datetime import datetime


class SystemTime:
    """
    System date/time should not change during an evaluation of a FHIRPath
    expression. It remains the same for the entire expression evaluation.
    """

    def __init__(self) -> None:
        self.expressionExecutionDateTime = datetime.now()

    def now(self):
        return self.expressionExecutionDateTime

    def reset(self):
        self.expressionExecutionDateTime = datetime.now()


class Constants:
    """
    These are values that should not change during an evaluation of a FHIRPath
    expression (e.g. the return value of today(), per the spec.)  They are
    constant during at least one evaluation.
    """

    today = None
    now = None
    timeOfDay = None
    localTimezoneOffset = None

    def reset(self):
        self.today = None
        self.now = None
        self.timeOfDay = None
        self.localTimezoneOffset = None
        systemtime.reset()


constants = Constants()
systemtime = SystemTime()
