import json
import yaml
import pytest

from tests.context import models
from tests.resources import resources
from fhirpathpy import evaluate


def pytest_collect_file(parent, path):
    if path.ext == ".yaml":
        return YamlFile.from_parent(parent, fspath=path)


class YamlFile(pytest.File):
    def collect(self):
        raw = yaml.safe_load(self.fspath.open())

        suites = raw["tests"]
        subject = raw["subject"] if "subject" in raw else None

        return self.collect_tests(suites, subject)

    def is_group(self, test):
        if not isinstance(test, dict):
            return False

        return any(key.startswith("group") for key in test.keys())

    def collect_tests(self, suites, subject):
        for suite in suites:
            if self.is_group(suite):
                name = next(iter(suite))
                tests = suite[name]
                for test in self.collect_tests(tests, subject):
                    yield test
            else:
                for test in self.collect_test(suite, subject):
                    yield test

    def collect_test(self, test, subject):
        name = test["desc"] if "desc" in test else ""
        is_disabled = "disable" in test and test["disable"]

        if "expression" in test and not is_disabled:
            yield YamlItem.from_parent(
                self, name=name, test=test, resource=subject,
            )


class YamlItem(pytest.Item):
    def __init__(self, name, parent, test, resource=None):
        super().__init__(name, parent)

        self.test = test
        self.resource = resource

    def runtest(self):

        expression = self.test["expression"]
        resource = self.resource

        model = models[self.test["model"]] if "model" in self.test else None

        if "inputfile" in self.test:
            if self.test["inputfile"] in resources:
                resource = resources[self.test["inputfile"]]

        context = {}

        if "error" in self.test and self.test["error"]:
            with pytest.raises(Exception):
                evaluate(resource, expression, context, model)
        else:
            assert evaluate(resource, expression, context, model) == self.test["result"]
