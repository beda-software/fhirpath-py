from typing import Literal

import pydantic
import pytest

from fhirpathpy import compile_as_array, compile_as_first


class CustomModel:
    pass


class HumanName(pydantic.BaseModel):
    given: list[str]
    family: str


class ContactPoint(pydantic.BaseModel):
    system: Literal["phone", "email", "fax", "pager", "url", "sms", "other"]
    value: str
    use: Literal["home", "work", "temp", "old", "mobile"]


class Patient(pydantic.BaseModel):
    resourceType: Literal["Patient"] = "Patient"  # noqa: N815
    name: list[HumanName]
    telecom: list[ContactPoint]


class Observation(pydantic.BaseModel):
    resourceType: Literal["Observation"] = "Observation"  # noqa: N815


class BundleEntry(pydantic.BaseModel):
    resource: Patient | Observation


class Bundle(pydantic.BaseModel):
    resourceType: Literal["Bundle"] = "Bundle"  # noqa: N815
    type: Literal["searchset"]
    entry: list[BundleEntry]


CUSTOM_MODEL = CustomModel()
PATIENT_DATA = {
    "resourceType": "Patient",
    "name": [
        {"given": ["First", "Middle"], "family": "Last"},
    ],
    "telecom": [
        {"system": "phone", "value": "555-555-2003", "use": "work"},
        {"system": "phone", "value": "555-555-2001", "use": "home"},
    ],
}
PATIENT_RESOURCE = Patient(**PATIENT_DATA)
BUNDLE_RESOURCE = Bundle(type="searchset", entry=[BundleEntry(resource=PATIENT_RESOURCE)])

EXPRESSION = "Patient.name.given"


@pytest.mark.parametrize(
    ("resource", "path", "input_type", "output_type", "expected"),
    [
        (PATIENT_DATA, EXPRESSION, dict, str, "First"),
        (PATIENT_RESOURCE, EXPRESSION, Patient, str, "First"),
        (PATIENT_DATA, "Patient.gender", dict, str, None),
        (
            BUNDLE_RESOURCE,
            "Bundle.entry.resource.where(resourceType='Patient')",
            Bundle,
            Patient,
            PATIENT_RESOURCE,
        ),
    ],
)
def compile_as_first_test(resource, path, input_type, output_type, expected):
    wrapper_fn = compile_as_first(path, input_type, output_type)
    result = wrapper_fn(resource)
    assert isinstance(result, output_type) or result is None
    assert result == expected


@pytest.mark.parametrize(
    ("resource", "path", "input_type", "output_type", "expected"),
    [
        (PATIENT_DATA, EXPRESSION, dict, str, ["First", "Middle"]),
        (PATIENT_RESOURCE, EXPRESSION, Patient, str, ["First", "Middle"]),
        (
            BUNDLE_RESOURCE,
            "Bundle.entry.resource.where(resourceType='Patient')",
            Bundle,
            Patient,
            [PATIENT_RESOURCE],
        ),
    ],
)
def compile_as_array_test(resource, path, input_type, output_type, expected):
    wrapper_fn = compile_as_array(path, input_type, output_type)
    result = wrapper_fn(resource)
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, output_type)
    assert result == expected


@pytest.mark.parametrize(
    ("resource", "path", "input_type", "output_type", "expected"),
    [
        (
            PATIENT_RESOURCE,
            EXPRESSION,
            Observation,
            str,
            "Resource type is Patient, expected Observation",
        ),
        (
            CUSTOM_MODEL,
            "Patient.name",
            type(CUSTOM_MODEL),
            str,
            "Don't know how to work with type CustomModel",
        ),
        (
            PATIENT_DATA,
            "Patient.telecom.value",
            dict,
            int,
            "Expected result to be int, but got str",
        ),
    ],
)
def exception_compile_as_first_test(resource, path, input_type, output_type, expected):
    wrapper_fn = compile_as_first(path, input_type, output_type)
    with pytest.raises(Exception) as exc:
        wrapper_fn(resource)
    assert str(exc.value) == expected


@pytest.mark.parametrize(
    ("resource", "path", "input_type", "output_type", "expected"),
    [
        (
            PATIENT_RESOURCE,
            EXPRESSION,
            Observation,
            str,
            "Resource type is Patient, expected Observation",
        ),
    ],
)
def exception_compile_as_array_test(resource, path, input_type, output_type, expected):
    wrapper_fn = compile_as_array(path, input_type, output_type)
    with pytest.raises(Exception) as exc:
        wrapper_fn(resource)
    assert str(exc.value) == expected
