import functools
import io
import sys

import pytest
from suby import run

from printo.reprs import _get_lambda_symbol, superrepr


def test_superrepr_basically_is_repr():

    assert superrepr(1) == "1"
    assert superrepr("hello") == "'hello'"
    assert superrepr([1, 2, 3]) == "[1, 2, 3]"
    assert superrepr({"a": 1, "b": 2}) == "{'a': 1, 'b': 2}"
    assert superrepr(None) == "None"
    assert superrepr(True) == "True"
    assert superrepr(False) == "False"
    assert superrepr(3.14) == "3.14"
    assert superrepr(1 + 2j) == "(1+2j)"
    assert superrepr([1, "hello", [2, 3]]) == "[1, 'hello', [2, 3]]"
    assert superrepr({"a": [1, 2], "b": {"c": 3}}) == "{'a': [1, 2], 'b': {'c': 3}}"


def test_superrepr_for_named_function():
    def function():
        pass

    assert superrepr(function) == "function"


def test_superrepr_for_lambda_function():
    assert superrepr(lambda x: x) == "lambda x: x"


def test_superrepr_for_lambda_functions_when_they_are_multple_in_one_line():
    lambdas = [lambda x: x, lambda y: y]

    assert superrepr(lambdas[0]) == "λ"
    assert superrepr(lambdas[1]) == "λ"


def test_lambda_symbol_unicode_terminal():
    assert _get_lambda_symbol() == 'λ'


def test_lambda_symbol_non_unicode_terminal():
    original_stdout = sys.stdout
    sys.stdout = io.TextIOWrapper(io.BytesIO(), encoding='ascii')
    try:
        _get_lambda_symbol.cache_clear()
        assert _get_lambda_symbol() == '<lambda>'
    finally:
        sys.stdout = original_stdout
        _get_lambda_symbol.cache_clear()


def test_superrepr_for_lambda_on_non_unicode_terminal():
    """
    When stdout encoding can't represent λ, superrepr must return '<lambda>'.

    Two lambdas on one line guarantee UncertaintyWithLambdasError on any Python version,
    so the encoding fallback is always reached.
    """
    result = run(
        sys.executable, '-c',
        'from printo import superrepr; f = [lambda x: x, lambda y: y][0]; print(superrepr(f))',
        catch_output=True,
        split=False,
        add_env={'PYTHONIOENCODING': 'ascii', 'PYTHONUTF8': '0'},
    )

    assert result.stdout.strip() == '<lambda>', f'stdout={result.stdout!r} stderr={result.stderr!r}'


@pytest.mark.skipif(sys.version_info >= (3, 13), reason='Python 3.13+ can introspect -c lambdas')
def test_superrepr_for_lambda_without_source_old_python():
    """
    On Python < 3.13, source of a lambda defined in -c is not retrievable.

    getclearsource raises OSError, and superrepr must fall back to 'λ'.
    """
    result = run(
        sys.executable, '-c',
        'from printo import superrepr; print(superrepr(lambda value, extra: False))',
        catch_output=True,
        split=False,
        add_env={'PYTHONUTF8': '1'},
    )

    assert result.stdout.strip() == 'λ', f'stdout={result.stdout!r} stderr={result.stderr!r}'


@pytest.mark.skipif(sys.version_info < (3, 13), reason='Python < 3.13 cannot introspect -c lambdas')
def test_superrepr_for_lambda_without_source_new_python():
    """On Python 3.13+, source introspection for -c lambdas works, so superrepr returns the actual source code."""
    result = run(
        sys.executable, '-c',
        'from printo import superrepr; print(superrepr(lambda value, extra: False))',
        catch_output=True,
        split=False,
        add_env={'PYTHONUTF8': '1'},
    )

    assert result.stdout.strip() == 'lambda value, extra: False', f'stdout={result.stdout!r} stderr={result.stderr!r}'


def test_superrepr_for_async_function():
    async def function():
        pass

    assert superrepr(function) == "function"


def test_superrepr_for_bound_method():
    class SomeClass:
        def method(self):
            pass

    assert superrepr(SomeClass().method) == "method"


def test_superrepr_for_async_bound_method():
    class SomeClass:
        async def method(self):
            pass

    assert superrepr(SomeClass().method) == "method"


def test_superrepr_for_static_method():
    class SomeClass:
        @staticmethod
        def method():
            pass

    assert superrepr(SomeClass.method) == "method"
    assert superrepr(SomeClass().method) == "method"


def test_superrepr_for_class_method():
    class SomeClass:
        @classmethod
        def method(cls):
            pass

    assert superrepr(SomeClass.method) == "method"
    assert superrepr(SomeClass().method) == "method"


def test_superrepr_for_partial():
    def function(a, b, c):
        pass

    assert superrepr(functools.partial(function, 1, 2)) == "functools.partial(function, 1, 2)"
    assert superrepr(functools.partial(function, 1, 2, 3)) == "functools.partial(function, 1, 2, 3)"
    assert superrepr(functools.partial(function, 1, c=3)) == "functools.partial(function, 1, c=3)"


def test_superrepr_for_partial_with_lambda():
    assert superrepr(functools.partial(lambda x, y: x + y, 1)) == "functools.partial(lambda x, y: x + y, 1)"


def test_superrepr_for_partial_with_class():
    class SomeClass:
        pass

    assert superrepr(functools.partial(SomeClass)) == "functools.partial(SomeClass)"


def test_superrepr_for_object_with_broken_repr():
    class BrokenRepr:
        def __repr__(self):
            raise RuntimeError("repr is broken")

    assert superrepr(BrokenRepr()) == "<BrokenRepr's object>"


def test_superrepr_for_object_with_repr_raising_different_exceptions():
    class RaisesValueError:
        def __repr__(self):
            raise ValueError("value error")

    class RaisesTypeError:
        def __repr__(self):
            raise TypeError("type error")

    class RaisesAttributeError:
        def __repr__(self):
            raise AttributeError("attr error")

    class RaisesRecursionError:
        def __repr__(self):
            raise RecursionError("recursion error")

    assert superrepr(RaisesValueError()) == "<RaisesValueError's object>"
    assert superrepr(RaisesTypeError()) == "<RaisesTypeError's object>"
    assert superrepr(RaisesAttributeError()) == "<RaisesAttributeError's object>"
    assert superrepr(RaisesRecursionError()) == "<RaisesRecursionError's object>"


def test_superrepr_for_object_with_broken_repr_and_broken_type():
    class BrokenMeta(type):
        @property
        def __name__(cls):
            raise RuntimeError("name is broken")

    class BrokenEverything(metaclass=BrokenMeta):
        def __repr__(self):
            raise RuntimeError("repr is broken")

    assert superrepr(BrokenEverything()) == "<unprintable>"


def test_superrepr_for_class_with_broken_name():
    """
    When __name__ raises, superrepr falls through to repr().

    type.__repr__ reads the class name via the C-level tp_name slot, bypassing
    Python-level __getattribute__, so repr() succeeds and returns the standard
    class repr string like "<class '...BadNameClass'>".
    """
    class BadNameMeta(type):
        def __getattribute__(cls, name: str) -> object:
            if name == '__name__':
                raise RuntimeError('broken __name__')
            return super().__getattribute__(name)

    class BadNameClass(metaclass=BadNameMeta):
        pass

    expected = "<class 'tests.units.test_reprs.test_superrepr_for_class_with_broken_name.<locals>.BadNameClass'>"
    assert superrepr(BadNameClass) == expected
    assert superrepr(BadNameClass) == repr(BadNameClass)
