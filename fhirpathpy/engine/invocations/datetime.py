from fhirpathpy.engine.invocations.constants import constants
from fhirpathpy.engine.nodes import FP_DateTime, FP_Time, FP_Date


def now(ctx, data):
    if not constants.now:
        now = constants.nowDate
        if not now.tzinfo:
            now = now.astimezone()
        isoStr = now.replace(microsecond=0).isoformat()  # YYYY-MM-DDThh:mm:ss+zz:zz
        constants.now = FP_DateTime(isoStr).timeMatchData
    return constants.now


def today(ctx, data):
    if not constants.today:
        now = constants.nowDate
        isoStr = now.date().isoformat()  # YYYY-MM-DD
        constants.today = FP_Date(isoStr).timeMatchData
    return constants.today


def timeOfDay(ctx, data):
    if not constants.timeOfDay:
        now = constants.nowDate
        isoStr = now.time().replace(microsecond=0).isoformat()  # hh:mm:ss
        constants.timeOfDay = FP_Time(isoStr).timeMatchData
    return constants.timeOfDay
