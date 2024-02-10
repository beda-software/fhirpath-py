from fhirpathpy.engine.invocations.constants import constants, systemtime
from fhirpathpy.engine.nodes import FP_DateTime, FP_Time


def now(ctx, data):
    if not constants.now:
        now = systemtime.now()
        if not now.tzinfo:
            now = now.astimezone()
        isoStr = now.isoformat()  # YYYY-MM-DDThh:mm:ss.ffffff+zz:zz
        constants.now = str(FP_DateTime(isoStr))
    return constants.now


def today(ctx, data):
    if not constants.today:
        now = systemtime.now()
        isoStr = now.date().isoformat()  # YYYY-MM-DD
        constants.today = str(FP_DateTime(isoStr))
    return constants.today


def timeOfDay(ctx, data):
    if not constants.timeOfDay:
        now = systemtime.now()
        isoStr = now.time().isoformat()  # hh:mm:ss.ffffff
        constants.timeOfDay = str(FP_Time(isoStr))
    return constants.timeOfDay
