import json
import pytest
from pathlib import Path
from fhirpathpy.parser import parse
from antlr4.error.Errors import LexerNoViableAltException

ast_fixtures_path = Path(__file__).resolve().parent.joinpath("fixtures").joinpath("ast")


def load_ast_fixture(fixture_name):
    fixture_path = ast_fixtures_path.joinpath(fixture_name + ".json")
    with open(fixture_path) as f:
        return json.load(f)


def are_ast_equal(first_ast, second_ast):
    first_string = json.dumps(first_ast, sort_keys=True)
    second_string = json.dumps(second_ast, sort_keys=True)

    return first_string == second_string


@pytest.mark.parametrize(
    "expression",
    [
        "4+4",
        "object",
        "object.method()",
        "object.method(42)",
        "object.property",
        "object.property.method()",
        "object.property.method(42)",
    ],
)
def parse_valid_test(expression):
    assert parse(expression) != {}


def parse_non_valid_test():
    with pytest.raises(LexerNoViableAltException):
        parse("!")


@pytest.mark.parametrize(
    "expression",
    [
        "%v+2",
        "a.b+2",
        "Observation.value",
        "Patient.name.given",
    ],
)
def output_correct_ast_test(expression):
    assert are_ast_equal(parse(expression), load_ast_fixture(expression))
