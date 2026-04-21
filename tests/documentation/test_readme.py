import functools

from printo import describe_call, not_none, superrepr


def test_basic_usage():
    assert describe_call('MyClassName', (1, 2, 'some text'), {'variable_name': 1, 'second_variable_name': 'kek'}) == "MyClassName(1, 2, 'some text', variable_name=1, second_variable_name='kek')"


def test_basic_filtering():
    assert describe_call(
        'MyClassName',
        (1, 2, 'some text'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
        filters={1: lambda x: x != 2, 'second_variable_name': lambda x: False},  # noqa: ARG005
    ) == "MyClassName(1, 'some text', variable_name=1)"


def test_filtering_of_nones():
    assert describe_call(
        'MyClassName',
        (1, None),
        {},
        filters={1: not_none},
    ) == 'MyClassName(1)'


def test_custom_serializator():
    assert describe_call(
        'MyClassName',
        (1, 2, 'lol'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
        serializer=lambda x: repr(x * 2),
    ) == "MyClassName(2, 4, 'lollol', variable_name=2, second_variable_name='kekkek')"


def test_superrepr_directly():
    def my_function():
        pass

    class MyClass:
        def my_method(self):
            pass

    assert superrepr(my_function) == 'my_function'
    assert superrepr(MyClass) == 'MyClass'
    assert superrepr(MyClass().my_method) == 'my_method'
    assert superrepr(functools.partial(my_function)) == 'functools.partial(my_function)'


def test_placeholders():
    assert describe_call(
        'MySuperClass',
        (1, 2, 'lol'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
        placeholders={
            1: '***',
            'variable_name': '***',
        },
    ) == "MySuperClass(1, ***, 'lol', variable_name=***, second_variable_name='kek')"


def test_item_limit():
    assert describe_call(
        'MyClass',
        (123456789,),
        {'name': 'a very long string'},
        item_limit=5,
    ) == "MyClass(12345..., name='a ver'...)"


def test_total_limit():
    assert describe_call(
        'MyClass',
        (),
        {'a': 1, 'b': 2, 'c': 3},
        total_limit=15,
    ) == 'MyClass(a=1, ...)'


def test_repred_conditional_expression():
    from printo import repred  # noqa: PLC0415

    @repred
    class SomeClass:
        def __init__(self, a: int, b: str) -> None:
            self.a = a if a is not None else 0
            self.b = b

    assert repr(SomeClass(42, 'hello')) == "SomeClass(a=42, b='hello')"
