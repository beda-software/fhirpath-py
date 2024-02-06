import copy
import datetime
from freezegun import freeze_time
import pytest
from fhirpathpy import evaluate


def datetime_tostring_tzinfo_test():
    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    # tz_offset = datetime.timezone(datetime.timedelta(hours=2))
    with freeze_time(
        lambda: datetime.datetime(
            year=2020,
            month=8,
            day=20,
            hour=17,
            minute=52,
            second=15,
            microsecond=123456,
            tzinfo=local_tz,
        )
    ):
        assert evaluate({}, "(now() + 1 month).toString()")[0] == "2020-09-20T17:52:15.123+00:00"


@pytest.mark.parametrize(
    ("resource", "path"),
    [
        (
            {
                "resourceType": "Patient",
                "name": [{"given": ["First", "Middle"], "family": "Last"}],
            },
            "Patient.name.given.toDate()",
        ),
    ],
)
def path_functions_test(resource, path):
    with pytest.raises(Exception) as e:
        evaluate(resource, path)
    assert str(e.value) == "to_date called for a collection of length 2"


def copy_deepcopy_test():
    copy_1 = copy.copy(evaluate({}, "@2018"))
    copy_2 = evaluate({}, "@2018").copy()

    deepcopy_1 = copy.deepcopy(evaluate({}, "@2018"))

    assert copy_1[0] == "2018"
    assert copy_2[0] == "2018"
    assert deepcopy_1[0] == "2018"
