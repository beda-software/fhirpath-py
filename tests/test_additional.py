import copy

import pytest

from fhirpathpy import evaluate


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


def evaluate_does_not_mutate_float_values_test():
    """evaluate() must not convert floats to Decimal in the caller's dict."""
    qr = {
        "resourceType": "QuestionnaireResponse",
        "status": "completed",
        "item": [
            {
                "linkId": "temperature",
                "answer": [
                    {
                        "valueQuantity": {
                            "value": 37.2,
                            "unit": "°C",
                            "system": "http://unitsofmeasure.org",
                            "code": "Cel",
                        }
                    }
                ],
            }
        ],
    }
    evaluate(qr, "QuestionnaireResponse.repeat(item).answer")
    assert isinstance(qr["item"][0]["answer"][0]["valueQuantity"]["value"], float)


def copy_deepcopy_test():
    copy_1 = copy.copy(evaluate({}, "@2018"))
    copy_2 = evaluate({}, "@2018").copy()

    deepcopy_1 = copy.deepcopy(evaluate({}, "@2018"))

    assert copy_1[0] == "2018"
    assert copy_2[0] == "2018"
    assert deepcopy_1[0] == "2018"
