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
        == "%Source.entry[0].resource.expansion.contains.where(code=%Coding.code) != {}"
    )

    assert (
        str(dsl.Location.where(dsl.physicalType.coding.code << "817").name)
        == "Location.where(physicalType.coding.code contains '817').name"
    )
    assert (
        str(
            (
                (
                    dsl.env.QuestionnaireResponse.repeat(dsl.item)
                    .where(linkId="test-type")
                    .answer.children()
                    .Coding.code
                    == "trainingTest"
                )
                | (
                    dsl.env.QuestionnaireResponse.repeat(dsl.item)
                    .where(linkId="sample-set")
                    .answer.count()
                    == 6
                )
            ).not_()
        )
        == "(%QuestionnaireResponse.repeat(item).where(linkId='test-type').answer.children().Coding.code = 'trainingTest' or %QuestionnaireResponse.repeat(item).where(linkId='sample-set').answer.count() = 6).not()"
    )

    assert str(dsl.Patient.id + "foo") == "(Patient.id + 'foo')"
    assert str("/Patient/" + dsl.Patient.id) == "('/Patient/' + Patient.id)"
