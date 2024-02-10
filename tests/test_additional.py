import copy
from datetime import UTC, datetime
from unittest import mock

import pytest
from fhirpathpy import evaluate


@mock.patch("fhirpathpy.engine.invocations.datetime.datetime")
def datetime_tostring_tzinfo_test(datetime_mock):
    datetime_mock.now.return_value = datetime(
        2020, 8, 20, 17, 52, 15, 123000, tzinfo=UTC
    )
    assert evaluate({}, "now() + 1 month")[0] == "2020-09-20T17:52:15.123+00:00"


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
