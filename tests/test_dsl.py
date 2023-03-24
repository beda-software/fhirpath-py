from fhirpathpy import dsl


def dsl_test():
    assert str(dsl.Patient.id) == "Patient.id"
    assert (
        str(dsl.Patient.name.where(use="usual").given.first())
        == "Patient.name.where(use='usual').given.first()"
    )
    assert (
        str(
            dsl.env.Source.entry[0].resource.expansion.contains.where(code=dsl.env.Coding.code)
            != dsl.empty
        )
        == "%Source.entry[0].resource.expansion.contains.where(code=%Coding.code) !~ {}"
    )
