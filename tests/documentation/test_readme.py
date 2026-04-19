import functools

from printo import describe_data_object, not_none, superrepr


def test_basic_usage():
    assert describe_data_object('MyClassName', (1, 2, 'some text'), {'variable_name': 1, 'second_variable_name': 'kek'}) == "MyClassName(1, 2, 'some text', variable_name=1, second_variable_name='kek')"


def test_basic_filtering():
    assert describe_data_object(
        'MyClassName',
        (1, 2, 'some text'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
        filters={1: lambda x: x != 2, 'second_variable_name': lambda x: False},  # noqa: ARG005
    ) == "MyClassName(1, 'some text', variable_name=1)"


def test_filtering_of_nones():
    assert describe_data_object(
        'MyClassName',
        (1, None),
        {},
        filters={1: not_none},
    ) == 'MyClassName(1)'


def test_custom_serializator():
    assert describe_data_object(
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
    assert describe_data_object(
        'MySuperClass',
        (1, 2, 'lol'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
        placeholders={
            1: '***',
            'variable_name': '***',
        },
    ) == "MySuperClass(1, ***, 'lol', variable_name=***, second_variable_name='kek')"
