from fhirpathpy import compile_as_first, compile_as_array
import fhirpy_types_r4b as r4b

PATIENT_DATA = {
    "resourceType": "Patient",
    "name": [{"given": ["First", "Middle"], "family": "Last"}],
}

PATIENT_RESOURCE = r4b.Patient(**PATIENT_DATA)

EXPRESSION = "Patient.name.given"


def compile_as_first_with_dict_test():
    patient_given = compile_as_first(EXPRESSION, dict, str)
    assert patient_given(PATIENT_DATA) == "First"


def compile_as_first_with_resource_test():
    patient_given = compile_as_first(EXPRESSION, r4b.Patient, str)
    assert patient_given(PATIENT_RESOURCE) == "First"


def compile_as_array_with_dict_test():
    patient_given = compile_as_array(EXPRESSION, dict, list[str])
    assert patient_given(PATIENT_DATA) == ["First", "Middle"]


def compile_as_array_with_resource_test():
    patient_given = compile_as_array(EXPRESSION, r4b.Patient, list[str])
    assert patient_given(PATIENT_RESOURCE) == ["First", "Middle"]


def compile_as_first_exception_test():
    patient_given = compile_as_first(EXPRESSION, r4b.Observation, str)
    try:
        patient_given(PATIENT_RESOURCE)
        assert False, "Expected exception not raised"
    except Exception as e:
        assert str(e) == "Resource type is <class 'fhirpy_types_r4b.Patient'>, expected <class 'fhirpy_types_r4b.Observation'>"


def compile_as_array_exception_test():
    patient_given = compile_as_array(EXPRESSION, r4b.Observation, list[str])
    try:
        patient_given(PATIENT_RESOURCE)
        assert False, "Expected exception not raised"
    except Exception as e:
        assert str(e) == "Resource type is <class 'fhirpy_types_r4b.Patient'>, expected <class 'fhirpy_types_r4b.Observation'>"
