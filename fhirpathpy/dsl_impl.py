class DSL:
    path: str

    def __init__(self, prefix=None):
        self.path = prefix

    def __getattr__(self, attr):
        if self.path is None and attr == "empty":
            return DSL("{}")
        if self.path is None and attr == "env":
            return DSL("%")
        elif self.path == "%":
            return DSL(f"{self.path}{attr}")
        elif self.path is not None:
            return DSL(f"{self.path}.{attr}")
        else:
            return DSL(attr)

    def __getitem__(self, attr):
        return DSL(f"{self.path}[{attr}]")

    def __eq__(self, other):
        return DSL(f"{self.path} ~ {format_value(other)}")

    def __ne__(self, other):
        return DSL(f"{self.path} !~ {format_value(other)}")

    def __call__(self, **kwargs):
        args = build_args(kwargs)
        return DSL(f"{self.path}({args})")

    def __str__(self):
        return self.path


def format_value(value):
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def build_args(args):
    return ",".join(f"{k}={format_value(v)}" for k, v in args.items())
