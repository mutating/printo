import functools
import sys
from inspect import isclass, isfunction, ismethod
from typing import Any

from getsources import UncertaintyWithLambdasError, getclearsource


@functools.lru_cache(maxsize=None)
def _get_lambda_symbol() -> str:
    try:
        'λ'.encode(sys.stdout.encoding or 'utf-8')
        return 'λ'
    except UnicodeEncodeError:
        return '<lambda>'


def superrepr(value: Any) -> str:  # noqa: PLR0911
    if isfunction(value):
        result = value.__name__

        if result == '<lambda>':
            try:
                return getclearsource(value)
            except (UncertaintyWithLambdasError, OSError):
                return _get_lambda_symbol()

        return result

    if ismethod(value):
        return value.__name__

    if isclass(value):
        return value.__name__

    if isinstance(value, functools.partial):
        func_repr = superrepr(value.func)
        parts = [func_repr]
        parts.extend(superrepr(arg) for arg in value.args)
        parts.extend(f'{k}={superrepr(v)}' for k, v in value.keywords.items())
        return f'functools.partial({", ".join(parts)})'

    try:
        return repr(value)
    except Exception:  # noqa: BLE001
        try:
            return f"<{type(value).__name__}'s object>"
        except Exception:  # noqa: BLE001
            return '<unprintable>'
