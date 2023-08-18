from fhirpathpy.engine.invocations.constants import constants
from fhirpathpy.engine.nodes import FP_DateTime, FP_Time


def truncate_to_milliseconds(iso_str):
    """Converts a string with microseconds to a string with milliseconds."""
    if "." in iso_str:
        iso_str = iso_str[: iso_str.index(".") + 4] + iso_str[iso_str.index(".") + 7 :]
    return iso_str


def now(ctx, data):
    if not constants.now:
        now = constants.nowDate
        if not now.tzinfo:
            now = now.astimezone()
        isoStr = truncate_to_milliseconds(now.isoformat())  # YYYY-MM-DDThh:mm:ss.fff+zz:zz
        constants.now = FP_DateTime(isoStr).getDateTimeMatchStr()
    return constants.now


def today(ctx, data):
    if not constants.today:
        now = constants.nowDate
        isoStr = now.date().isoformat()  # YYYY-MM-DD
        constants.today = FP_DateTime(isoStr).getDateTimeMatchStr()
    return constants.today


def timeOfDay(ctx, data):
    if not constants.timeOfDay:
        now = constants.nowDate
        isoStr = truncate_to_milliseconds(now.time().isoformat())  # hh:mm:ss.fff
        constants.timeOfDay = FP_Time(isoStr).getTimeMatchStr()
    return constants.timeOfDay
