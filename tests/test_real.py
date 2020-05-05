from fhirpathpy import evaluate


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
