from fhirpathpy import evaluate, compile
import pickle

def find_concept_test():
    env = {}
    env["Source"] = {
        "resourceType": "Bundle",
        "id": -1,
        "entry": [
            {
                "resource": {
                    "resourcceType": "ValueSet",
                    "expansion": {
                        "contains": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "16291000122106",
                                "display": "Ifenprodil",
                            },
                            {
                                "system": "http://snomed.info/sct",
                                "code": "789067004",
                                "display": "Amlodipine benzoate",
                            },
                            {
                                "system": "http://snomed.info/sct",
                                "code": "783132009",
                                "display": "Bosentan hydrochloride",
                            },
                            {
                                "system": "http://snomed.info/sct",
                                "code": "766924002",
                                "display": "Substance with nicotinic receptor antagonist mechanism of action",
                            },
                            {
                                "system": "http://snomed.info/sct",
                                "code": "708177006",
                                "display": "Betahistine mesilate (substance)",
                            },
                        ]
                    },
                }
            }
        ],
    }

    env["Coding"] = {
        "system": "http://snomed.info/sct",
        "code": "708177006",
        "display": "Betahistine mesilate (substance)",
    }

    assert evaluate(
        {},
        "%Source.entry[0].resource.expansion.contains.where(code=%Coding.code)!~{}",
        env,
    ) == [True]

    env["Coding"] = (
        {
            "system": "http://snomed.info/sct",
            "code": "428159003",
            "display": "Ambrisentan",
        },
    )

    assert evaluate(
        {},
        "%Source.entry[0].resource.expansion.contains.where(code=%Coding.code)!~{}",
        env,
    ) == [False]


def aidbox_polimorphici_test():
    qr = {
        "resourceType": "QuestionnaireResponse",
        "item": {"linkId": "foo", "answer": {"value": {"Coding": {"code": 1}}}},
    }
    assert evaluate(qr, "QuestionnaireResponse.item.answer.value.Coding") == [
        {"code": 1}
    ]


def pickle_test():
    resource = {
        "resourceType": "DiagnosticReport",
        "id": "abc",
        "subject": {"reference": "Patient/cdf"},
    }
    path = compile(path="DiagnosticReport.subject.reference")

    dumped = pickle.dumps(path)
    reload = pickle.loads(dumped)

    assert reload(resource) == ["Patient/cdf"]


def extension_test():
    patient = {
        "identifier": [
            {
                "period": {
                    "start": "2020-01-01"
                },
                "system": "http://hl7.org/fhir/sid/us-mbi",
                "type": {
                    "coding": [
                        {
                            "code": "MC",
                            "display": "Patient's Medicare number",
                            "extension": [
                                {
                                    "url": "https://bluebutton.cms.gov/resources/codesystem/identifier-currency",
                                    "valueCoding": {
                                        "code": "current",
                                        "display": "Current",
                                        "system": "https://bluebutton.cms.gov/resources/codesystem/identifier-currency"
                                    }
                                }
                            ],
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203"
                        }
                    ]
                },
                "value": "7SM0A00AA00"
            }
        ],
        "resourceType": "Patient"
    }
    result = evaluate(patient, "Patient.identifier.where(type.coding.extension('https://bluebutton.cms.gov/resources/codesystem/identifier-currency').valueCoding.code = 'current').where(system = 'http://hl7.org/fhir/sid/us-mbi').value")
    assert result == ["7SM0A00AA00"]
