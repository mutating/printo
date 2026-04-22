import pytest
from full_match import match
from sigmatch import SignatureMismatchError

from printo import repred
from printo.filters import not_none


@pytest.mark.mypy_testing
def test_repred_bare_decorator():
    """mypy infers the exact decorated class type, not Any or object."""
    @repred
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_empty_parens():
    """mypy infers the exact decorated class type when @repred() is called with empty parens."""
    @repred()
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_with_prefer_positional():
    """mypy infers the exact decorated class type when prefer_positional=True is passed."""
    @repred(prefer_positional=True)
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_with_qualname():
    """mypy infers the exact decorated class type when qualname=True is passed."""
    @repred(qualname=True)
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_with_ignore():
    """mypy infers the exact decorated class type when ignore=[...] is passed."""
    @repred(ignore=['x'])
    class Foo:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    _: Foo = Foo(1, 2)


@pytest.mark.mypy_testing
def test_repred_with_getters():
    """mypy infers the exact decorated class type when getters={...} is passed."""
    @repred(getters={'x': lambda self: self.x})
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_with_filters():
    """mypy infers the exact decorated class type when filters={...} is passed."""
    @repred(filters={'x': not_none})
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_with_positionals():
    """mypy infers the exact decorated class type when positionals=[...] is passed."""
    @repred(positionals=['x'])
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_with_multiple_kwargs():
    """mypy infers the exact decorated class type when multiple keyword args are passed."""
    @repred(prefer_positional=True, qualname=True)
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_with_varargs():
    """mypy infers the exact decorated class type on a class with *args and **kwargs."""
    @repred
    class Foo:
        def __init__(self, a: int, b: int, *args: int, **kwargs: str) -> None:
            self.a = a
            self.b = b
            self.args = args
            self.kwargs = kwargs

    _: Foo = Foo(1, 2)


@pytest.mark.mypy_testing
def test_repred_instance_type():
    """mypy infers Foo instance type, not object or Any, after bare @repred."""
    @repred
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: Foo = Foo(1)


@pytest.mark.mypy_testing
def test_repred_instance_wrong_type():
    """mypy rejects assigning a @repred-decorated class instance to an incompatible type."""
    @repred
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: str = Foo(1)  # E: [assignment]


@pytest.mark.mypy_testing
def test_repred_instance_wrong_type_with_kwargs():
    """mypy rejects wrong-type assignment even when @repred is called with keyword args."""
    @repred(prefer_positional=True)
    class Foo:
        def __init__(self, x: int) -> None:
            self.x = x

    _: str = Foo(1)  # E: [assignment]


@pytest.mark.mypy_testing
def test_repred_invalid_filter_value_type():
    """
    mypy rejects a non-callable filters value as dict-item error.

    The pytest.raises wrapper is needed because repred also validates types at runtime.
    """
    with pytest.raises(SignatureMismatchError, match=match('You have defined a getter for parameter "x" that cannot be called with a single argument.')):
        @repred(filters={'x': 42})  # E: [dict-item]
        class Foo:
            def __init__(self, x: int) -> None:
                self.x = x


@pytest.mark.mypy_testing
def test_repred_invalid_getter_value_type():
    """
    mypy rejects a non-callable getters value as dict-item error.

    The pytest.raises wrapper is needed because repred also validates types at runtime.
    """
    with pytest.raises(SignatureMismatchError, match=match('You have defined a getter for parameter "x" that cannot be called with a single argument (an object of class Foo).')):
        @repred(getters={'x': 'not_a_function'})  # E: [dict-item]
        class Foo:
            def __init__(self, x: int) -> None:
                self.x = x


@pytest.mark.mypy_testing
def test_repred_invalid_filter_key_type():
    """
    mypy rejects a float filters key as dict-item error.

    The pytest.raises wrapper is needed because repred also validates types at runtime.
    """
    with pytest.raises(ValueError, match=match('Keys for a filtered dictionary can be either integers starting from 0 or strings (parameter names).')):
        @repred(filters={1.5: not_none})  # E: [dict-item]
        class Foo:
            def __init__(self, x: int) -> None:
                self.x = x


@pytest.mark.mypy_testing
def test_repred_invalid_ignore_element_type():
    """
    mypy rejects a non-str element in the ignore list as list-item error.

    The pytest.raises wrapper is needed because repred also validates types at runtime.
    """
    with pytest.raises(AttributeError, match=match("'int' object has no attribute 'isidentifier'")):
        @repred(ignore=[1])  # E: [list-item]
        class Foo:
            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y


@pytest.mark.mypy_testing
def test_repred_invalid_positionals_element_type():
    """
    mypy rejects a non-str element in the positionals list as list-item error.

    The pytest.raises wrapper is needed because repred also validates types at runtime.
    """
    with pytest.raises(AttributeError, match=match("'int' object has no attribute 'isidentifier'")):
        @repred(positionals=[1])  # E: [list-item]
        class Foo:
            def __init__(self, x: int) -> None:
                self.x = x
