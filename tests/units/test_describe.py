from typing import Any

import pytest
from sigmatch.errors import SignatureMismatchError

from printo import describe_data_object, not_none


def test_empty_object():
    assert describe_data_object('ClassName', (), {}) == 'ClassName()'
    assert describe_data_object('ClassName', (), {}, serializer=lambda x: 'kek') == 'ClassName()'  # noqa: ARG005


@pytest.mark.parametrize(
    'args_converter',
    [
        lambda x: x,
        list,
    ],
)
def test_only_args(args_converter):
    assert describe_data_object('ClassName', args_converter((1, 2, 3)), {}) == 'ClassName(1, 2, 3)'
    assert describe_data_object('ClassName', args_converter((1, 2)), {}) == 'ClassName(1, 2)'
    assert describe_data_object('ClassName', args_converter((1,)), {}) == 'ClassName(1)'

    assert describe_data_object('ClassName', args_converter(('lol', 'kek')), {}) == "ClassName('lol', 'kek')"
    assert describe_data_object('ClassName', args_converter(('lol',)), {}) == "ClassName('lol')"

    assert describe_data_object('ClassName', args_converter(('lol', 1, 2, 3)), {}) == "ClassName('lol', 1, 2, 3)"
    assert describe_data_object('ClassName', args_converter(('lol', 1, 2, 3, 'kek')), {}) == "ClassName('lol', 1, 2, 3, 'kek')"
    assert describe_data_object('ClassName', args_converter(('lol', 1, 2, 3, 'kek', None)), {}) == "ClassName('lol', 1, 2, 3, 'kek', None)"


def test_only_kwargs():
    assert describe_data_object('ClassName', (), {'lol': 1, 'kek': 2}) == 'ClassName(lol=1, kek=2)'

    assert describe_data_object('ClassName', (), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName(lol='insert text', kek='insert the second text')"

    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"


def test_args_and_kwargs():
    assert describe_data_object('ClassName', (1, 2, 3), {'lol': 1, 'kek': 2}) == 'ClassName(1, 2, 3, lol=1, kek=2)'
    assert describe_data_object('ClassName', (1, 2, 3), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName(1, 2, 3, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', (1, 2, 3), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName(1, 2, 3, number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', (1, 2, 3), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName(1, 2, 3, number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"

    assert describe_data_object('ClassName', ('lol', 'kek'), {'lol': 1, 'kek': 2}) == "ClassName('lol', 'kek', lol=1, kek=2)"
    assert describe_data_object('ClassName', ('lol', 'kek'), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 'kek', lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', ('lol', 'kek'), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 'kek', number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', ('lol', 'kek'), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName('lol', 'kek', number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"

    assert describe_data_object('ClassName', ('lol', 1, 2, 3), {'lol': 1, 'kek': 2}) == "ClassName('lol', 1, 2, 3, lol=1, kek=2)"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName('lol', 1, 2, 3, number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"

    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek'), {'lol': 1, 'kek': 2}) == "ClassName('lol', 1, 2, 3, 'kek', lol=1, kek=2)"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek'), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, 'kek', lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek'), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, 'kek', number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek'), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName('lol', 1, 2, 3, 'kek', number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"

    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {'lol': 1, 'kek': 2}) == "ClassName('lol', 1, 2, 3, 'kek', None, lol=1, kek=2)"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, 'kek', None, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, 'kek', None, number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName('lol', 1, 2, 3, 'kek', None, number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"


def test_set_serializator_for_args():
    assert describe_data_object('ClassName', (1, 2, 3), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(11, 22, 33)'
    assert describe_data_object('ClassName', (1, 2), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(11, 22)'
    assert describe_data_object('ClassName', (1,), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(11)'

    assert describe_data_object('ClassName', ('lol', 'kek'), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol, kekkek)'
    assert describe_data_object('ClassName', ('lol',), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol)'

    assert describe_data_object('ClassName', ('lol', 1, 2, 3), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol, 11, 22, 33)'
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek'), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol, 11, 22, 33, kekkek)'
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol, 11, 22, 33, kekkek, NoneNone)'

    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, serializer=lambda x: f'{x}{x}', placeholders={1: 'kek'}) == 'ClassName(lollol, kek, 22, 33, kekkek, NoneNone)'


def test_set_serializator_for_kwargs():
    assert describe_data_object('ClassName', (), {'lol': 1, 'kek': 2}, serializer=lambda x: f'{x}{x}') == 'ClassName(lol=11, kek=22)'

    assert describe_data_object('ClassName', (), {'lol': 'insert text', 'kek': 'insert the second text'}, serializer=lambda x: f'{x}{x}') == 'ClassName(lol=insert textinsert text, kek=insert the second textinsert the second text)'

    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}, serializer=lambda x: f'{x}{x}') == 'ClassName(number_1=11, number_2=22, lol=insert textinsert text, kek=insert the second textinsert the second text)'
    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}, serializer=lambda x: f'{x}{x}') == 'ClassName(number_1=11, number_2=22, lol=insert textinsert text, kek=insert the second textinsert the second text, number_3=33)'

    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}, serializer=lambda x: f'{x}{x}', placeholders={'lol': 'kek'}) == 'ClassName(number_1=11, number_2=22, lol=kek, kek=insert the second textinsert the second text, number_3=33)'


def test_set_empty_filters_dict_for_args():
    assert describe_data_object('ClassName', (1, 2, 3), {}, filters={}) == 'ClassName(1, 2, 3)'
    assert describe_data_object('ClassName', (1, 2), {}, filters={}) == 'ClassName(1, 2)'
    assert describe_data_object('ClassName', (1,), {}, filters={}) == 'ClassName(1)'

    assert describe_data_object('ClassName', ('lol', 'kek'), {}, filters={}) == "ClassName('lol', 'kek')"
    assert describe_data_object('ClassName', ('lol',), {}, filters={}) == "ClassName('lol')"

    assert describe_data_object('ClassName', ('lol', 1, 2, 3), {}, filters={}) == "ClassName('lol', 1, 2, 3)"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek'), {}, filters={}) == "ClassName('lol', 1, 2, 3, 'kek')"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, filters={}) == "ClassName('lol', 1, 2, 3, 'kek', None)"


def test_set_filters_dict_with_empty_lambdas_for_args():
    def allow_all(x):  # noqa: ARG001
        return True

    assert describe_data_object('ClassName', (1, 2, 3), {}, filters={0: allow_all, 1: allow_all, 2: allow_all}) == 'ClassName(1, 2, 3)'
    assert describe_data_object('ClassName', (1, 2), {}, filters={0: allow_all, 1: allow_all}) == 'ClassName(1, 2)'
    assert describe_data_object('ClassName', (1,), {}, filters={0: allow_all}) == 'ClassName(1)'

    assert describe_data_object('ClassName', ('lol', 'kek'), {}, filters={0: allow_all, 1: allow_all}) == "ClassName('lol', 'kek')"
    assert describe_data_object('ClassName', ('lol',), {}, filters={0: allow_all}) == "ClassName('lol')"

    assert describe_data_object('ClassName', ('lol', 1, 2, 3), {}, filters={0: allow_all, 1: allow_all, 2: allow_all}) == "ClassName('lol', 1, 2, 3)"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek'), {}, filters={0: allow_all, 1: allow_all, 2: allow_all, 3: allow_all}) == "ClassName('lol', 1, 2, 3, 'kek')"
    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, filters={0: allow_all, 1: allow_all, 2: allow_all, 3: allow_all, 4: allow_all}) == "ClassName('lol', 1, 2, 3, 'kek', None)"


def test_set_real_filters_for_args():
    def not_all(x):  # noqa: ARG001
        return False

    assert describe_data_object('ClassName', (1, 2, 3), {}, filters={0: not_all, 1: not_all, 2: not_all}) == 'ClassName()'
    assert describe_data_object('ClassName', (1,), {}, filters={0: not_all}) == 'ClassName()'
    assert describe_data_object('ClassName', ('lol', 'kek'), {}, filters={0: not_all, 1: not_all}) == "ClassName()"
    assert describe_data_object('ClassName', ('lol',), {}, filters={0: not_all}) == "ClassName()"

    assert describe_data_object('ClassName', (1, 2, 3), {}, filters={0: not_all}) == 'ClassName(2, 3)'
    assert describe_data_object('ClassName', (1, 2, 3), {}, filters={2: not_all}) == 'ClassName(1, 2)'
    assert describe_data_object('ClassName', (1, 2, 3), {}, filters={1: not_all}) == 'ClassName(1, 3)'
    assert describe_data_object('ClassName', (1, 2), {}, filters={0: not_all}) == 'ClassName(2)'
    assert describe_data_object('ClassName', (1, 2), {}, filters={1: not_all}) == 'ClassName(1)'
    assert describe_data_object('ClassName', (1, 2, 3), {}, filters={3: not_all}) == 'ClassName(1, 2, 3)'

    assert describe_data_object('ClassName', ('lol', 'kek'), {}, filters={0: not_all}) == "ClassName('kek')"
    assert describe_data_object('ClassName', ('lol', 'kek'), {}, filters={1: not_all}) == "ClassName('lol')"
    assert describe_data_object('ClassName', ('lol',), {}, filters={1: not_all}) == "ClassName('lol')"


def test_args_filters_are_getting_values():
    fields = []

    def add_to_fields(value: Any) -> bool:
        fields.append(value)
        return True

    assert describe_data_object('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, filters={0: add_to_fields, 1: add_to_fields, 2: add_to_fields, 3: add_to_fields, 4: add_to_fields, 5: add_to_fields}) == "ClassName('lol', 1, 2, 3, 'kek', None)"

    assert fields == ['lol', 1, 2, 3, 'kek', None]


def test_kwargs_filters_are_getting_values():
    fields = []

    def add_to_fields(value: Any) -> bool:
        fields.append(value)
        return True

    assert describe_data_object('ClassName', (), {'lol': 'kek', 'kek': 'lol'}, filters={'lol': add_to_fields, 'kek': add_to_fields}) == "ClassName(lol='kek', kek='lol')"

    assert fields == ['kek', 'lol']


def test_set_empty_filters_dict_for_kwargs():
    assert describe_data_object('ClassName', (), {'lol': 1, 'kek': 2}, filters={}) == 'ClassName(lol=1, kek=2)'

    assert describe_data_object('ClassName', (), {'lol': 'insert text', 'kek': 'insert the second text'}, filters={}) == "ClassName(lol='insert text', kek='insert the second text')"

    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}, filters={}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}, filters={}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"


def test_set_filters_dict_with_empty_lambdas_for_kwargs():
    def allow_all(x):  # noqa: ARG001
        return True

    assert describe_data_object('ClassName', (), {'lol': 1, 'kek': 2}, filters={'lol': allow_all, 'kek': allow_all}) == 'ClassName(lol=1, kek=2)'

    assert describe_data_object('ClassName', (), {'lol': 'insert text', 'kek': 'insert the second text'}, filters={'lol': allow_all, 'kek': allow_all}) == "ClassName(lol='insert text', kek='insert the second text')"

    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}, filters={'lol': allow_all, 'kek': allow_all}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_data_object('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}, filters={'lol': allow_all, 'kek': allow_all}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"


def test_set_real_filters_for_kwargs():
    def not_all(x):  # noqa: ARG001
        return False

    assert describe_data_object('ClassName', (), {'lol': 1, 'kek': 2}, filters={'lol': not_all, 'kek': not_all}) == 'ClassName()'
    assert describe_data_object('ClassName', (), {'lol': 1, 'kek': 2}, filters={'lol': not_all}) == 'ClassName(kek=2)'
    assert describe_data_object('ClassName', (), {'lol': 1, 'kek': 2}, filters={'kek': not_all}) == 'ClassName(lol=1)'


def test_set_real_filters_for_args_and_kwargs():
    def not_all(x):  # noqa: ARG001
        return False

    assert describe_data_object('ClassName', (1, 2), {'lol': 1, 'kek': 2}, filters={'lol': not_all, 'kek': not_all, 0: not_all, 1: not_all}) == 'ClassName()'


def test_filter_not_nones():
    assert describe_data_object('ClassName', (1, 'lol', None), {'lol': 1, 'kek': None}, filters={'lol': not_none, 'kek': not_none, 0: not_none, 1: not_none, 2: not_none}) == "ClassName(1, 'lol', lol=1)"


def test_named_functions_as_arguments():
    def function():
        pass

    assert describe_data_object('ClassName', (1, 2, 3, function), {}) == 'ClassName(1, 2, 3, function)'
    assert describe_data_object('ClassName', (function,), {}) == 'ClassName(function)'
    assert describe_data_object('ClassName', (function,), {'function': function}) == 'ClassName(function, function=function)'
    assert describe_data_object('ClassName', (), {'function': function}) == 'ClassName(function=function)'
    assert describe_data_object('ClassName', (1, 2, 3, function), {'function': function}) == 'ClassName(1, 2, 3, function, function=function)'


def test_lambdas_as_arguments():
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {}) == 'ClassName(1, 2, 3, lambda x: x)'
    assert describe_data_object('ClassName', (lambda x: x,), {}) == 'ClassName(lambda x: x)'
    assert describe_data_object('ClassName', (lambda x: x,), {'function': lambda x: x}) == 'ClassName(λ, function=λ)'
    assert describe_data_object('ClassName', (), {'function': lambda x: x}) == 'ClassName(function=lambda x: x)'
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'function': lambda x: x}) == 'ClassName(1, 2, 3, λ, function=λ)'


def test_simple_placeholders():
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek'}, placeholders={}) == 'ClassName(1, 2, 3, lambda x: x, lol=\'kek\')'
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek'}, placeholders=None) == 'ClassName(1, 2, 3, lambda x: x, lol=\'kek\')'
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek'}, placeholders={'lol': '***'}) == 'ClassName(1, 2, 3, lambda x: x, lol=***)'
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '***'}) == 'ClassName(1, 2, 3, lambda x: x, lol=***, kek=\'lol\')'
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '***', 0: '***'}) == 'ClassName(***, 2, 3, lambda x: x, lol=***, kek=\'lol\')'
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '***', 0: '***', 3: '***'}) == 'ClassName(***, 2, 3, ***, lol=***, kek=\'lol\')'
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '***', 0: '***', 3: '***', 'kek': '&'}) == 'ClassName(***, 2, 3, ***, lol=***, kek=&)'
    assert describe_data_object('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '🔒', 0: '***', 3: '***', 'kek': '&'}) == 'ClassName(***, 2, 3, ***, lol=🔒, kek=&)'


def test_wrong_serializator_callback():
    with pytest.raises(SignatureMismatchError):
        describe_data_object('ClassName', (1, 2, 3), {'lol': 'kek'}, serializer=lambda x, y: x + y)


def test_wrong_filter_callback():
    with pytest.raises(SignatureMismatchError):
        describe_data_object('ClassName', (), {'lol': 1, 'kek': 2}, filters={'kek': lambda x, y: x + y})

    with pytest.raises(SignatureMismatchError):
        describe_data_object('ClassName', (1, 2, 3), {}, filters={0: lambda x, y: x + y})


def test_print_classes():
    class SomeClass:
        pass

    assert describe_data_object('ClassName', (int, str, SomeClass), {'lol': int, 'kek': str, 'cheburek': SomeClass}) == 'ClassName(int, str, SomeClass, lol=int, kek=str, cheburek=SomeClass)'


def test_async_function_as_argument():
    async def function():
        pass

    assert describe_data_object('ClassName', (function,), {}) == 'ClassName(function)'
    assert describe_data_object('ClassName', (), {'function': function}) == 'ClassName(function=function)'


def test_broken_repr_as_argument():
    class BrokenRepr:
        def __repr__(self):
            raise RuntimeError("repr is broken")

    broken = BrokenRepr()
    assert describe_data_object('ClassName', (broken,), {}) == 'ClassName(<BrokenRepr>)'
    assert describe_data_object('ClassName', (), {'x': broken}) == 'ClassName(x=<BrokenRepr>)'
    assert describe_data_object('ClassName', (1, broken, 2), {'x': broken}) == 'ClassName(1, <BrokenRepr>, 2, x=<BrokenRepr>)'


def test_item_limit_basic():
    # superrepr(12345) = '12345' (5 chars); item_limit=2 -> '12...'
    assert describe_data_object('C', (12345,), {}, item_limit=2) == 'C(12...)'
    assert describe_data_object('C', (), {'x': 12345}, item_limit=2) == 'C(x=12...)'


def test_item_limit_not_exceeded():
    # '12345' has 5 chars; item_limit=5 -> no truncation
    assert describe_data_object('C', (12345,), {}, item_limit=5) == 'C(12345)'
    # item_limit=4 -> '1234...'
    assert describe_data_object('C', (12345,), {}, item_limit=4) == 'C(1234...)'


def test_item_limit_zero():
    # item_limit=0 -> value fully replaced with '...'
    assert describe_data_object('C', (12345,), {}, item_limit=0) == 'C(...)'
    assert describe_data_object('C', (), {'x': 12345}, item_limit=0) == 'C(x=...)'


def test_item_limit_with_kwargs():
    # limit applies only to the value part, not to 'key=value' as a whole
    assert describe_data_object('C', (), {'key': 12345}, item_limit=2) == 'C(key=12...)'


def test_item_limit_negative():
    with pytest.raises(ValueError, match='item_limit must be a non-negative integer'):
        describe_data_object('C', (1,), {}, item_limit=-1)


def test_item_limit_with_placeholder():
    # item_limit applies to placeholder strings too
    assert describe_data_object('C', (1,), {}, item_limit=2, placeholders={0: 'secret'}) == 'C(se...)'


def test_total_limit_basic():
    # 'C(a=1, b=2, c=3)' = 16 chars; total_limit=11 -> 'C(a=1, ...)' = 11 chars
    assert describe_data_object('C', (), {'a': 1, 'b': 2, 'c': 3}, total_limit=11) == 'C(a=1, ...)'


def test_total_limit_not_exceeded():
    result = describe_data_object('C', (1, 2), {}, total_limit=100)
    assert result == 'C(1, 2)'
    assert len(result) <= 100


def test_total_limit_drops_to_ellipsis_only():
    # First item doesn't fit — result is ClassName(...)
    # 'Name(x=12345)' = 13 chars; total_limit=9 = minimum for 'Name' -> 'Name(...)'
    assert describe_data_object('Name', (), {'x': 12345}, total_limit=9) == 'Name(...)'


def test_total_limit_minimum():
    # Exactly len(class_name) + 5 is the minimum valid total_limit
    name = 'A'
    minimum = len(name) + 5  # = 6
    result = describe_data_object(name, (1, 2, 3), {}, total_limit=minimum)
    assert result == 'A(...)'
    assert len(result) == minimum


def test_total_limit_too_small():
    with pytest.raises(ValueError, match='total_limit'):
        describe_data_object('ClassName', (1,), {}, total_limit=5)


def test_total_limit_negative():
    with pytest.raises(ValueError, match='total_limit must be a non-negative integer'):
        describe_data_object('C', (1,), {}, total_limit=-1)


def test_total_limit_with_item_limit():
    # item_limit=2 truncates '12345' -> '12...', '1' stays as '1'
    # chunks: ['a=1', 'b=12...'] -> full: 'C(a=1, b=12...)' = 15 chars
    # total_limit=11: k=1 -> 'C(a=1, ...)' = 11 chars <= 11 ✓
    assert describe_data_object('C', (), {'a': 1, 'b': 12345}, item_limit=2, total_limit=11) == 'C(a=1, ...)'


def test_total_limit_first_item_too_long():
    # First and only item exceeds total_limit -> 'C(...)'
    # 'C(a=12345)' = 10 chars; total_limit=6 = minimum -> 'C(...)'
    assert describe_data_object('C', (), {'a': 12345}, total_limit=6) == 'C(...)'


def test_total_limit_exact_fit():
    # 'A(1, 2, 3)' = 10 chars; total_limit=10 -> no truncation
    result = describe_data_object('A', (1, 2, 3), {})
    assert result == 'A(1, 2, 3)'
    assert describe_data_object('A', (1, 2, 3), {}, total_limit=len(result)) == result


def test_item_limit_string_basic():
    # repr('hello world') = "'hello world'" = 13 chars; item_limit=7
    # N=5: repr('hello') = "'hello'" = 7 chars <= 7; N=6: repr('hello ') = 8 > 7
    assert describe_data_object('C', ('hello world',), {}, item_limit=7) == "C('hello'...)"
    assert describe_data_object('C', (), {'name': 'hello world'}, item_limit=7) == "C(name='hello'...)"


def test_item_limit_string_at_minimum():
    # item_limit=2 fits only repr('') = "''" = 2 chars
    assert describe_data_object('C', ('abc',), {}, item_limit=2) == "C(''...)"


def test_item_limit_string_below_minimum():
    # item_limit=1: repr('') = "''" = 2 > 1, so fall back to truncating the repr
    # repr('abc') = "'abc'" -> first 1 char = "'" + '...' = "'..."
    assert describe_data_object('C', ('abc',), {}, item_limit=1) == "C('...)"


def test_item_limit_string_not_exceeded():
    # repr('hi') = "'hi'" = 4 chars; item_limit=4 -> no truncation
    assert describe_data_object('C', ('hi',), {}, item_limit=4) == "C('hi')"
    # item_limit=5 -> still no truncation
    assert describe_data_object('C', ('hi',), {}, item_limit=5) == "C('hi')"


def test_item_limit_string_with_escape_chars():
    # repr('a\nb') = "'a\\nb'" = 6 chars; item_limit=5
    # N=2: repr('a\n') = "'a\\n'" = 5 chars <= 5; N=3: repr('a\nb') = 6 > 5
    assert describe_data_object('C', ('a\nb',), {}, item_limit=5) == "C('a\\n'...)"


def test_item_limit_string_custom_serializer():
    # Custom serializer: str(x) gives 'hello' (no quotes)
    # 'hello' != repr('hello') = "'hello'", so old truncation applies
    assert describe_data_object('C', ('hello',), {}, serializer=lambda x: str(x), item_limit=3) == 'C(hel...)'
