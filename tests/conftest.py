import json
import yaml
import pytest
import itertools

import tests.context.r4 as r4
import tests.context.stu3 as stu3

from fhirpathpy import evaluate


models = {
    "r4": r4.model,
    "stu3": stu3.model,
}


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
        if "expression" in test:
            yield YamlItem.from_parent(
                self, name=name, test=test, resource=subject,
            )


class YamlItem(pytest.Item):
    def __init__(self, name, parent, test, resource):
        super().__init__(name, parent)

        self.test = test
        self.resource = resource

    def runtest(self):
        model = models[self.test["model"]] if "model" in self.test else None
        expression = self.test["expression"]

        context = {}

        if "error" in self.test and self.test["error"]:
            with pytest.raises(Exception):
                evaluate(self.resource, expression, context, model)
        else:
            assert (
                evaluate(self.resource, expression, context, model)
                == self.test["result"]
            )
