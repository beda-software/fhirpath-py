from fhirpathpy import compile_as_first, compile_as_array
import fhirpy_types_r4b as r4b
import pytest

PATIENT_DATA = {
    "resourceType": "Patient",
    "name": [{"given": ["First", "Middle"], "family": "Last"}],
}

PATIENT_RESOURCE = r4b.Patient(**PATIENT_DATA)

EXPRESSION = "Patient.name.given"

@pytest.mark.parametrize(
    ("fn", "resource", "path", "input_type", "output_type", "expected"),
    [
        (compile_as_first, PATIENT_DATA, EXPRESSION, dict, str, "First"),
        (compile_as_first, PATIENT_RESOURCE, EXPRESSION, r4b.Patient, str, "First"),
        (compile_as_array, PATIENT_DATA, EXPRESSION, dict, list[str], ["First", "Middle"]),
        (compile_as_array, PATIENT_RESOURCE, EXPRESSION, r4b.Patient, list[str], ["First", "Middle"]),
    ],
)
def compile_as_test(fn, resource, path, input_type, output_type, expected):
    wrapper_fn = fn(path, input_type, output_type)
    assert wrapper_fn(resource) == expected


@pytest.mark.parametrize(
    ("fn", "resource", "path", "input_type", "output_type", "expected"),
    [
        (compile_as_first, PATIENT_RESOURCE, EXPRESSION, r4b.Observation, str, "Resource type is <class 'fhirpy_types_r4b.Patient'>, expected <class 'fhirpy_types_r4b.Observation'>"),
        (compile_as_array, PATIENT_RESOURCE, EXPRESSION, r4b.Observation, list[str], "Resource type is <class 'fhirpy_types_r4b.Patient'>, expected <class 'fhirpy_types_r4b.Observation'>"),
    ],
)
def exception_compile_as_test(fn, resource, path, input_type, output_type, expected):
    wrapper_fn = fn(path, input_type, output_type)
    try:
        wrapper_fn(resource)
        assert False, "Expected exception not raised"
    except Exception as e:
        assert str(e) == expected
