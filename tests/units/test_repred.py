import pytest
from full_match import match
from sigmatch import SignatureMismatchError

from printo import ParameterMappingNotFoundError, RedefinitionError, repred


def test_apply_decorator_to_wrong_object():
    with pytest.raises(ValueError, match=match('The @repred decorator can only be applied to classes.')):
        repred(123)

    with pytest.raises(ValueError, match=match('The @repred decorator can only be applied to classes.')):
        @repred
        def function():
            ...

def test_redefenition():
    class First:
        def __repr__(self):
            return 'First()'

    class Second(First):
        ...

    with pytest.raises(RedefinitionError, match=match('Class First already has its own __repr__ method defined; you cannot override it.')):
        repred(First)

    repred(Second)

    assert repr(Second()) == 'Second()'


def test_empty_class():
    @repred
    class SomeClass:
        ...

    assert repr(SomeClass()) == 'SomeClass()'


def test_usual_usage():
    @repred
    class Class1:
        def __init__(self):
            ...

    @repred
    class Class2:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    assert repr(Class1()) == 'Class1()'

    assert repr(Class2(1, 2)) == 'Class2(a=1, b=2)'
    assert repr(Class2(1, 2, 3)) == 'Class2(a=1, b=2, c=3)'
    assert repr(Class2(1, 2, c=3)) == 'Class2(a=1, b=2, c=3)'


def test_self_renamed():
    @repred
    class Class1:
        def __init__(kek):  # noqa: N805
            ...

    @repred
    class Class2:
        def __init__(kek, a, b, c=None):  # noqa: N805
            kek.a = a
            kek.b = b
            kek.c = c

    assert repr(Class1()) == 'Class1()'

    assert repr(Class2(1, 2)) == 'Class2(a=1, b=2)'
    assert repr(Class2(1, 2, 3)) == 'Class2(a=1, b=2, c=3)'
    assert repr(Class2(1, 2, c=3)) == 'Class2(a=1, b=2, c=3)'


def test_usual_usage_when_prefer_positionals():
    @repred(prefer_positional=True)
    class Class1:
        def __init__(self):
            ...

    @repred(prefer_positional=True)
    class Class2:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    assert repr(Class1()) == 'Class1()'

    assert repr(Class2(1, 2)) == 'Class2(1, 2)'
    assert repr(Class2(1, 2, 3)) == 'Class2(1, 2, 3)'
    assert repr(Class2(1, 2, c=3)) == 'Class2(1, 2, 3)'


def test_impossible_custom_getter():
    with pytest.raises(SignatureMismatchError, match=match('You have defined a getter for parameter "a" that cannot be called with a single argument (an object of class Class1).')):
        @repred(getters={'a': lambda: 5})
        class Class1:
            def __init__(self, a):
                ...

    with pytest.raises(SignatureMismatchError, match=match('You have defined a getter for parameter "a" that cannot be called with a single argument (an object of class Class2).')):
        @repred(getters={'a': lambda x, y: 5})  # noqa: ARG005
        class Class2:
            def __init__(self, a):
                ...


def test_custom_getter_with_wrong_name():
    with pytest.raises(NameError, match=match('Parameter "a" is not used when initializing objects of class SomeClass, but you have defined a getter for it.')):
        @repred(getters={'a': lambda x: 5})  # noqa: ARG005
        class SomeClass:
            def __init__(self):
                ...


def test_set_custom_getters():
    @repred(getters={'a': lambda x: 5})  # noqa: ARG005
    class Class1:
        def __init__(self, a):
            ...

    @repred(getters={'a': lambda x: 5})  # noqa: ARG005
    class Class2:
        def __init__(self, a):
            self.a = a

    assert repr(Class1(1)) == 'Class1(a=5)'


def test_missing_parameters():
    with pytest.raises(ParameterMappingNotFoundError, match=match('No internal object property or custom getter were found for the parameter a.')):
        @repred
        class Class1:
            def __init__(self, a):
                ...

    with pytest.raises(ParameterMappingNotFoundError, match=match('No internal object properties or custom getters were found for the parameters a, b.')):
        @repred
        class Class2:
            def __init__(self, a, b):
                ...


def test_positional_only_parameters():
    @repred
    class Class1:
        def __init__(self, a, b, c=None, /):
            self.a = a
            self.b = b
            self.c = c

    @repred
    class Class2:
        def __init__(self, a, b, /, c=None):
            self.a = a
            self.b = b
            self.c = c

    @repred(prefer_positional=True)
    class Class3:
        def __init__(self, a, b, /, c=None):
            self.a = a
            self.b = b
            self.c = c

    assert repr(Class1(1, 2)) == 'Class1(1, 2)'
    assert repr(Class1(1, 2, 3)) == 'Class1(1, 2, 3)'

    assert repr(Class2(1, 2)) == 'Class2(1, 2)'
    assert repr(Class2(1, 2, 3)) == 'Class2(1, 2, c=3)'
    assert repr(Class2(1, 2, c=3)) == 'Class2(1, 2, c=3)'

    assert repr(Class3(1, 2)) == 'Class3(1, 2)'
    assert repr(Class3(1, 2, 3)) == 'Class3(1, 2, 3)'
    assert repr(Class3(1, 2, c=3)) == 'Class3(1, 2, 3)'


def test_keyword_only_parameters():
    @repred
    class Class1:
        def __init__(self, *, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    @repred
    class Class2:
        def __init__(self, a, b, *, c=None):
            self.a = a
            self.b = b
            self.c = c

    @repred(prefer_positional=True)
    class Class3:
        def __init__(self, a, b, *, c=None):
            self.a = a
            self.b = b
            self.c = c

    assert repr(Class1(a=1, b=2)) == 'Class1(a=1, b=2)'
    assert repr(Class1(a=1, b=2, c=3)) == 'Class1(a=1, b=2, c=3)'

    assert repr(Class2(1, 2)) == 'Class2(a=1, b=2)'
    assert repr(Class2(1, 2, c=3)) == 'Class2(a=1, b=2, c=3)'

    assert repr(Class3(1, 2)) == 'Class3(1, 2)'
    assert repr(Class3(1, 2, c=3)) == 'Class3(1, 2, c=3)'


def test_star_args():
    @repred
    class Class1:
        def __init__(self, *args):
            self.args = args

    @repred
    class Class2:
        def __init__(self, a, b, c=None, *args):
            self.a = a
            self.b = b
            self.c = c
            self.args = args

    assert repr(Class1()) == 'Class1()'
    assert repr(Class1(1, 2, 3)) == 'Class1(1, 2, 3)'
    assert repr(Class1(1, 2, 3, lambda x: x)) == 'Class1(1, 2, 3, lambda x: x)'

    assert repr(Class2(1, 2)) == 'Class2(1, 2)'
    assert repr(Class2(1, 2, 3)) == 'Class2(1, 2, 3)'
    assert repr(Class2(1, 2, c=3)) == 'Class2(1, 2, 3)'
    assert repr(Class2(1, 2, 3, 4, 5)) == 'Class2(1, 2, 3, 4, 5)'


def test_star_kwargs():
    @repred
    class Class1:
        def __init__(self, **kwargs):
            self.args = kwargs

    @repred
    class Class2:
        def __init__(self, a, b, c=None, **kwargs):
            self.a = a
            self.b = b
            self.c = c
            self.args = kwargs

    @repred(prefer_positional=True)
    class Class3:
        def __init__(self, a, b, c=None, **kwargs):
            self.a = a
            self.b = b
            self.c = c
            self.args = kwargs

    assert repr(Class1()) == 'Class1()'
    assert repr(Class1(a=1, b=2, c=3)) == 'Class1(a=1, b=2, c=3)'
    assert repr(Class1(a=1, b=2, c=3, d=lambda x: x)) == 'Class1(a=1, b=2, c=3, d=lambda x: x)'

    assert repr(Class2(1, 2)) == 'Class2(a=1, b=2)'
    assert repr(Class2(1, 2, 3)) == 'Class2(a=1, b=2, c=3)'
    assert repr(Class2(1, 2, c=3)) == 'Class2(a=1, b=2, c=3)'
    assert repr(Class2(1, 2, 3, d=4, e=5)) == 'Class2(a=1, b=2, c=3, d=4, e=5)'

    assert repr(Class3(1, 2)) == 'Class3(1, 2)'
    assert repr(Class3(1, 2, 3)) == 'Class3(1, 2, 3)'
    assert repr(Class3(1, 2, c=3)) == 'Class3(1, 2, 3)'
    assert repr(Class3(1, 2, 3, d=4, e=5)) == 'Class3(1, 2, 3, d=4, e=5)'
