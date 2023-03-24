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

    ### TODO
    assert (
        str(dsl.env.Location.where('817' in dsl.env.physicalType.coding.code).name)
        == "Location.where(physicalType.coding.code contains '817').name"
    )
    """

    (%QuestionnaireResponse.repeat(item).where(linkId='test-type').answer.children().Coding.code = 'trainingTest' or %QuestionnaireResponse.repeat(item).where(linkId='sample-set').answer.count() = 6).not()
    """
