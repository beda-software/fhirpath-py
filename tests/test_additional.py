import datetime
from freezegun import freeze_time
from fhirpathpy import evaluate


def datetime_tostring_tzinfo_test():
    tz_offset = datetime.timezone(datetime.timedelta(hours=2))
    with freeze_time(
        lambda: datetime.datetime(
            year=2020,
            month=8,
            day=20,
            hour=17,
            minute=52,
            second=15,
            microsecond=123456,
            tzinfo=tz_offset,
        )
    ):
        assert evaluate({}, "(now() + 1 month).toString()")[0] == "2020-09-20T13:52:15.123+00:00"
