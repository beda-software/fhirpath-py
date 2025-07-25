from fhirpathpy import evaluate as fhirpath
from decimal import Decimal


def use_decimal_in_context_test():
    assert fhirpath(
        {},
        "%QuestionnaireResponse.repeat(item).where(linkId='blood-pressure-systolic').answer.valueQuantity",
        {
            "QuestionnaireResponse": {
                "resourceType": "QuestionnaireResponse",
                "item": [
                    {
                        "answer": [{"valueQuantity": {"value": Decimal(120)}}],
                        "linkId": "blood-pressure-systolic",
                    }
                ],
            }
        },
    ) == [{"value": Decimal(120)}]
