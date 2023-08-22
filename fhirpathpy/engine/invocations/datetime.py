from fhirpathpy.engine.invocations.constants import constants
from fhirpathpy.engine.nodes import FP_DateTime, FP_Time


def now(ctx, data):
    if not constants.now:
        now = constants.nowDate
        if not now.tzinfo:
            now = now.astimezone()
        isoStr = now.isoformat()  # YYYY-MM-DDThh:mm:ss.ffffff+zz:zz
        constants.now = FP_DateTime(isoStr)
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
        isoStr = now.time().isoformat()  # hh:mm:ss.ffffff
        constants.timeOfDay = FP_Time(isoStr)
    return constants.timeOfDay
