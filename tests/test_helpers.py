from fhirpathpy import compile_as_first, compile_as_array
import fhirpy_types_r4b as r4b

PATIENT_DATA = {
    "resourceType": "Patient",
    "name": [{"given": ["First", "Middle"], "family": "Last"}],
}

PATIENT_RESOURCE = r4b.Patient(**PATIENT_DATA)


def compile_as_first_with_dict_test():
    patient_given = compile_as_first("Patient.name.given")
    assert patient_given(PATIENT_DATA) == "First"


def compile_as_first_with_resource_test():
    patient_given = compile_as_first("Patient.name.given", r4b.Patient)
    assert patient_given(PATIENT_RESOURCE) == "First"


def compile_as_array_with_dict_test():
    patient_given = compile_as_array("Patient.name.given")
    assert patient_given(PATIENT_DATA) == ["First", "Middle"]


def compile_as_array_with_resource_test():
    patient_given = compile_as_array("Patient.name.given", r4b.Patient)
    assert patient_given(PATIENT_RESOURCE) == ["First", "Middle"]


def compile_as_first_exception_test():
    patient_given = compile_as_first("Patient.name.given", r4b.Observation)
    try:
        patient_given(PATIENT_RESOURCE)
        assert False, "Expected exception not raised"
    except Exception as e:
        assert str(e) == "Resource is not of type <class 'fhirpy_types_r4b.Observation'>"


def compile_as_array_exception_test():
    patient_given = compile_as_array("Patient.name.given", r4b.Observation)
    try:
        patient_given(PATIENT_RESOURCE)
        assert False, "Expected exception not raised"
    except Exception as e:
        assert str(e) == "Resource is not of type <class 'fhirpy_types_r4b.Observation'>"
