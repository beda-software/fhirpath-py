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
            if attr == "not_":
                return DSL(f"{self.path}.not")
            return DSL(f"{self.path}.{attr}")
        else:
            return DSL(attr)

    def __getitem__(self, attr):
        return DSL(f"{self.path}[{attr}]")

    def __eq__(self, other):
        return DSL(f"{self.path} = {format_value(other)}")

    def __ne__(self, other):
        return DSL(f"{self.path} != {format_value(other)}")

    def __lshift__(self, item):
        return DSL(f"{self.path} contains {format_value(item)}")

    def __or__(self, item):
        return DSL(f"({self.path} or {format_value(item)})")

    def __not__(self):
        return DSL(f"{self.path}.not()")

    def __call__(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return DSL(f"{self.path}()")
        elif len(args) == 0 and len(kwargs) == 1:
            arg = build_args(kwargs)
            return DSL(f"{self.path}({arg})")
        elif len(args) == 1 and len(kwargs) == 0:
            arg = format_value(args[0])
            return DSL(f"{self.path}({arg})")
        else:
            raise Exception(f"Wrong arguements args={args} kwargs={kwargs}")

    def __str__(self):
        return self.path

    def __add__(self, item):
        return DSL(f"({self.path} + {format_value(item)})")

    def __radd__(self, item):
        return DSL(f"({format_value(item)} + {self.path})")


def format_value(value):
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def build_args(args):
    return ",".join(f"{k}={format_value(v)}" for k, v in args.items())
