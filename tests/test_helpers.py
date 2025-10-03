from fhirpathpy import compile_as_first, compile_as_array


PATIENT_DATA = {
    "resourceType": "Patient",
    "name": [{"given": ["First", "Middle"], "family": "Last"}],
}


def compile_as_first_test():
    patient_given = compile_as_first("Patient.name.given")
    assert patient_given(PATIENT_DATA) == "First"


def compile_as_array_test():
    patient_given = compile_as_array("Patient.name.given")
    assert patient_given(PATIENT_DATA) == ["First", "Middle"]
