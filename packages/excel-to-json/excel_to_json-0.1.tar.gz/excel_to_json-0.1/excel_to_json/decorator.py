from enum import Enum


class Decorator(Enum):
    Hook = 1
    Ref = 2
    Object = 3


def parse_decorator(decorator_str):
    decorator_type = None
    if decorator_str == '#object':
        decorator_type = Decorator.Object
    elif decorator_str == '#hook':
        decorator_type = Decorator.Hook
    elif decorator_str == '#ref':
        decorator_type = Decorator.Ref
    return decorator_type
