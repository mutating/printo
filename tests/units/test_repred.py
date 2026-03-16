import pytest
from full_match import match
from sigmatch import SignatureMismatchError

from printo import ParameterMappingNotFoundError, RedefinitionError, CanNotBePositionalError, repred


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
    with pytest.raises(ParameterMappingNotFoundError, match=match('No internal object property or custom getter was found for the parameter a.')):
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


def test_set_filters():
    @repred(filters={'x': lambda x: x})
    class Class1:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    assert repr(Class1(0, 0)) == 'Class1(y=0)'

    @repred(
        filters={1: lambda x: x},
        prefer_positional=True,
    )
    class Class2:
        def __init__(self, x, y):
            self.x = x
            self.y = y


    assert repr(Class2(0, 0)) == 'Class2(0)'

    @repred(
        filters={0: lambda x: x},
        prefer_positional=True,
    )
    class Class3:
        def __init__(self, *args):
            self.x = args

    assert repr(Class3(0, 0, 0)) == 'Class3(0, 0)'

    @repred(
        filters={0: lambda x: x},
        prefer_positional=True,
    )
    class Class4:
        def __init__(self, *args):
            self.x = args

    assert repr(Class3(0, 0, 0)) == 'Class3(0, 0)'


def test_qualname():
    @repred(qualname=True)
    class Class1:
        def __init__(self):
            ...

    @repred(qualname=True)
    class Class2:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    assert repr(Class1()) == 'test_qualname.<locals>.Class1()'

    assert repr(Class2(1, 2)) == 'test_qualname.<locals>.Class2(a=1, b=2)'
    assert repr(Class2(1, 2, 3)) == 'test_qualname.<locals>.Class2(a=1, b=2, c=3)'
    assert repr(Class2(1, 2, c=3)) == 'test_qualname.<locals>.Class2(a=1, b=2, c=3)'


def test_wrong_filters():
    with pytest.raises(ValueError, match=match('Keys for a filtered dictionary can be either integers starting from 0 or strings (parameter names).')):
        @repred(filters={...: lambda x: x})
        class SomeClass1: ...

    with pytest.raises(ValueError, match=match('Keys for a filtered dictionary can be either integers starting from 0 or strings (parameter names).')):
        @repred(filters={-1: lambda x: x})
        class SomeClass2: ...

    with pytest.raises(ValueError, match=match('Keys for a filtered dictionary can be either integers starting from 0 or strings (parameter names).')):
        @repred(filters={'lol kek': lambda x: x})
        class SomeClass3: ...

    with pytest.raises(SignatureMismatchError, match=match('You have defined a getter for parameter "name" that cannot be called with a single argument.')):
        @repred(filters={'name': lambda: False})
        class SomeClass4: ...

    with pytest.raises(SignatureMismatchError, match=match('You have defined a getter for parameter "0" that cannot be called with a single argument.')):
        @repred(filters={0: lambda: False})
        class SomeClass5: ...


def test_init_without_self():
    with pytest.raises(ParameterMappingNotFoundError, match=match('It seems that the "self" argument was not found for the __init__ method of class SomeClass.')):
        @repred
        class SomeClass:
            def __init__():
                ...


def test_ignore_wrong_identificator():
    with pytest.raises(ValueError, match=match('You have specified the parameter name \'lol kek\' to ignore, which is not a valid identifier name in Python.')):
        @repred(ignore=['lol kek'])
        class SomeClass:
            def __init__(self):
                ...

    with pytest.raises(NameError, match=match('Parameter "lol" is not used when initializing objects of class SomeClass2, but you have defined it as an ignored one.')):
        @repred(ignore=['lol'])
        class SomeClass2:
            def __init__(self):
                ...


def test_simple_ignore():
    @repred(ignore=['args'])
    class Class1:
        def __init__(self, *args):
            self.args = args

    @repred(ignore=['kwargs'])
    class Class2:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    @repred(ignore=['c'])
    class Class3:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    @repred(ignore=['a'])
    class Class4:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    assert repr(Class1()) == 'Class1()'
    assert repr(Class1(1, 2, 3)) == 'Class1()'

    assert repr(Class2(a=1, b=2, c=3)) == 'Class2()'

    assert repr(Class3(a=1, b=2, c=3)) == 'Class3(a=1, b=2)'

    assert repr(Class4(a=1, b=2, c=3)) == 'Class4(b=2, c=3)'


def test_conditional_expressions():
    with pytest.raises(ParameterMappingNotFoundError, match=match('No internal object property or custom getter was found for the parameter a.')):
        @repred
        class SomeClass:
            def __init__(self, a):
                self.a = a if a else 123


def test_set_wrong_positionals():
    with pytest.raises(ValueError, match=match('You have specified the parameter name \'lol kek\' as a positional, which is not a valid identifier name in Python.')):
        @repred(positionals=['lol kek'])
        class SomeClass:
            def __init__(self, a):
                self.a = a

    with pytest.raises(NameError, match=match('Parameter "lol" is not used when initializing objects of class SomeClass2, but you have defined it as a position one.')):
        @repred(positionals=['lol'])
        class SomeClass2:
            def __init__(self, a):
                self.a = a

    with pytest.raises(CanNotBePositionalError, match=match('Parameter a cannot be represented as a positional one.')):
        @repred(positionals=['a'])
        class SomeClass3:
            def __init__(self, *, a):
                self.a = a

    with pytest.raises(CanNotBePositionalError, match=match('Parameter a cannot be represented as a positional one.')):
        @repred(positionals=['a'])
        class SomeClass4:
            def __init__(self, **a):
                self.a = a

    with pytest.raises(CanNotBePositionalError, match=match('Parameter b cannot be represented as a positional one.')):
        @repred(positionals=['b', 'c'])
        class SomeClass5:
            def __init__(self, a, b, c=None):
                self.a = a
                self.b = b
                self.c = c

    with pytest.raises(CanNotBePositionalError, match=match('Parameter c cannot be represented as a positional one.')):
        @repred(positionals=['c'])
        class SomeClass5:
            def __init__(self, a, b, c=None):
                self.a = a
                self.b = b
                self.c = c


def test_positionals():
    @repred(positionals=['a'])
    class Class1:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    @repred(positionals=['a', 'b'])
    class Class2:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    @repred(positionals=['a', 'b', 'c'])
    class Class3:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    @repred(positionals=['b', 'c'], prefer_positional=True)
    class Class4:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    assert repr(Class1(1, 2)) == 'Class1(1, b=2)'
    assert repr(Class1(1, 2, 3)) == 'Class1(1, b=2, c=3)'
    assert repr(Class1(1, 2, c=3)) == 'Class1(1, b=2, c=3)'

    assert repr(Class2(1, 2)) == 'Class2(1, 2)'
    assert repr(Class2(1, 2, 3)) == 'Class2(1, 2, c=3)'
    assert repr(Class2(1, 2, c=3)) == 'Class2(1, 2, c=3)'

    assert repr(Class3(1, 2)) == 'Class3(1, 2)'
    assert repr(Class3(1, 2, 3)) == 'Class3(1, 2, 3)'
    assert repr(Class3(1, 2, c=3)) == 'Class3(1, 2, 3)'

    assert repr(Class4(1, 2)) == 'Class4(1, 2)'
    assert repr(Class4(1, 2, 3)) == 'Class4(1, 2, 3)'
    assert repr(Class4(1, 2, c=3)) == 'Class4(1, 2, 3)'
