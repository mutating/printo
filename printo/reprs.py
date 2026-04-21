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
    if isfunction(value) or ismethod(value) or isclass(value):
        result = value.__name__

        if isfunction(value) and result == '<lambda>':
            try:
                return getclearsource(value)
            except (UncertaintyWithLambdasError, OSError):
                return _get_lambda_symbol()

        return result

    if isinstance(value, functools.partial):
        from printo.describe import describe_data_object  # noqa: PLC0415

        return describe_data_object('functools.partial', (value.func, *value.args), value.keywords)

    try:
        return repr(value)
    except Exception:  # noqa: BLE001
        try:
            return f"<{type(value).__name__}'s object>"
        except Exception:  # noqa: BLE001
            return '<unprintable>'
