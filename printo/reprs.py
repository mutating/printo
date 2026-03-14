from inspect import isclass, isfunction
from typing import Any

from getsources import UncertaintyWithLambdasError, getclearsource


def superrepr(value: Any) -> str:
    if isfunction(value):
        result = value.__name__

        if result == '<lambda>':
            try:
                return getclearsource(value)
            except UncertaintyWithLambdasError:
                return 'λ'

        return result

    if isclass(value):
        return value.__name__

    return repr(value)
