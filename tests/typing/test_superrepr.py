import pytest
from full_match import match

from printo import superrepr


@pytest.mark.mypy_testing
def test_superrepr_with_int():
    """mypy accepts any object as argument and infers str return type."""
    _: str = superrepr(42)


@pytest.mark.mypy_testing
def test_superrepr_with_string():
    """mypy accepts a string argument and infers str return type."""
    _: str = superrepr('hello')


@pytest.mark.mypy_testing
def test_superrepr_with_lambda():
    """mypy accepts a lambda as argument and infers str return type."""
    _: str = superrepr(lambda x: x)


@pytest.mark.mypy_testing
def test_superrepr_with_function():
    """mypy accepts a regular function as argument and infers str return type."""
    def my_function() -> None:
        pass
    _: str = superrepr(my_function)


@pytest.mark.mypy_testing
def test_superrepr_with_class():
    """mypy accepts a class object as argument and infers str return type."""
    class MyClass:
        pass
    _: str = superrepr(MyClass)


@pytest.mark.mypy_testing
def test_superrepr_no_args():
    """mypy rejects a call with no arguments — value is required."""
    with pytest.raises(TypeError, match=match("superrepr() missing 1 required positional argument: 'value'")):
        superrepr()  # E: [call-arg]


@pytest.mark.mypy_testing
def test_superrepr_too_many_args():
    """mypy rejects a call with two positional arguments — only one is accepted."""
    with pytest.raises(TypeError, match=match('superrepr() takes 1 positional argument but 2 were given')):
        superrepr(1, 2)  # E: [call-arg]


@pytest.mark.mypy_testing
def test_superrepr_wrong_return_type():
    """mypy rejects assigning the superrepr return value to a non-str variable."""
    _: int = superrepr(42)  # E: [assignment]
