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


def test_print_classes():
    class SomeClass:
        pass

    assert describe_data_object('ClassName', (int, str, SomeClass), {'lol': int, 'kek': str, 'cheburek': SomeClass}) == 'ClassName(int, str, SomeClass, lol=int, kek=str, cheburek=SomeClass)'
