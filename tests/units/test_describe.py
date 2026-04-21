from typing import Any

import pytest
from sigmatch.errors import SignatureMismatchError

from printo import describe_call, not_none


def test_empty_object():
    assert describe_call('ClassName', (), {}) == 'ClassName()'
    assert describe_call('ClassName', (), {}, serializer=lambda x: 'kek') == 'ClassName()'  # noqa: ARG005


@pytest.mark.parametrize(
    'args_converter',
    [
        lambda x: x,
        list,
    ],
)
def test_only_args(args_converter):
    assert describe_call('ClassName', args_converter((1, 2, 3)), {}) == 'ClassName(1, 2, 3)'
    assert describe_call('ClassName', args_converter((1, 2)), {}) == 'ClassName(1, 2)'
    assert describe_call('ClassName', args_converter((1,)), {}) == 'ClassName(1)'

    assert describe_call('ClassName', args_converter(('lol', 'kek')), {}) == "ClassName('lol', 'kek')"
    assert describe_call('ClassName', args_converter(('lol',)), {}) == "ClassName('lol')"

    assert describe_call('ClassName', args_converter(('lol', 1, 2, 3)), {}) == "ClassName('lol', 1, 2, 3)"
    assert describe_call('ClassName', args_converter(('lol', 1, 2, 3, 'kek')), {}) == "ClassName('lol', 1, 2, 3, 'kek')"
    assert describe_call('ClassName', args_converter(('lol', 1, 2, 3, 'kek', None)), {}) == "ClassName('lol', 1, 2, 3, 'kek', None)"


def test_only_kwargs():
    assert describe_call('ClassName', (), {'lol': 1, 'kek': 2}) == 'ClassName(lol=1, kek=2)'

    assert describe_call('ClassName', (), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName(lol='insert text', kek='insert the second text')"

    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"


def test_args_and_kwargs():
    assert describe_call('ClassName', (1, 2, 3), {'lol': 1, 'kek': 2}) == 'ClassName(1, 2, 3, lol=1, kek=2)'
    assert describe_call('ClassName', (1, 2, 3), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName(1, 2, 3, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', (1, 2, 3), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName(1, 2, 3, number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', (1, 2, 3), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName(1, 2, 3, number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"

    assert describe_call('ClassName', ('lol', 'kek'), {'lol': 1, 'kek': 2}) == "ClassName('lol', 'kek', lol=1, kek=2)"
    assert describe_call('ClassName', ('lol', 'kek'), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 'kek', lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', ('lol', 'kek'), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 'kek', number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', ('lol', 'kek'), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName('lol', 'kek', number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"

    assert describe_call('ClassName', ('lol', 1, 2, 3), {'lol': 1, 'kek': 2}) == "ClassName('lol', 1, 2, 3, lol=1, kek=2)"
    assert describe_call('ClassName', ('lol', 1, 2, 3), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', ('lol', 1, 2, 3), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', ('lol', 1, 2, 3), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName('lol', 1, 2, 3, number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"

    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek'), {'lol': 1, 'kek': 2}) == "ClassName('lol', 1, 2, 3, 'kek', lol=1, kek=2)"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek'), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, 'kek', lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek'), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, 'kek', number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek'), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName('lol', 1, 2, 3, 'kek', number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"

    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {'lol': 1, 'kek': 2}) == "ClassName('lol', 1, 2, 3, 'kek', None, lol=1, kek=2)"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, 'kek', None, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}) == "ClassName('lol', 1, 2, 3, 'kek', None, number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}) == "ClassName('lol', 1, 2, 3, 'kek', None, number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"


def test_set_serializator_for_args():
    assert describe_call('ClassName', (1, 2, 3), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(11, 22, 33)'
    assert describe_call('ClassName', (1, 2), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(11, 22)'
    assert describe_call('ClassName', (1,), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(11)'

    assert describe_call('ClassName', ('lol', 'kek'), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol, kekkek)'
    assert describe_call('ClassName', ('lol',), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol)'

    assert describe_call('ClassName', ('lol', 1, 2, 3), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol, 11, 22, 33)'
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek'), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol, 11, 22, 33, kekkek)'
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, serializer=lambda x: f'{x}{x}') == 'ClassName(lollol, 11, 22, 33, kekkek, NoneNone)'

    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, serializer=lambda x: f'{x}{x}', placeholders={1: 'kek'}) == 'ClassName(lollol, kek, 22, 33, kekkek, NoneNone)'


def test_set_serializator_for_kwargs():
    assert describe_call('ClassName', (), {'lol': 1, 'kek': 2}, serializer=lambda x: f'{x}{x}') == 'ClassName(lol=11, kek=22)'

    assert describe_call('ClassName', (), {'lol': 'insert text', 'kek': 'insert the second text'}, serializer=lambda x: f'{x}{x}') == 'ClassName(lol=insert textinsert text, kek=insert the second textinsert the second text)'

    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}, serializer=lambda x: f'{x}{x}') == 'ClassName(number_1=11, number_2=22, lol=insert textinsert text, kek=insert the second textinsert the second text)'
    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}, serializer=lambda x: f'{x}{x}') == 'ClassName(number_1=11, number_2=22, lol=insert textinsert text, kek=insert the second textinsert the second text, number_3=33)'

    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}, serializer=lambda x: f'{x}{x}', placeholders={'lol': 'kek'}) == 'ClassName(number_1=11, number_2=22, lol=kek, kek=insert the second textinsert the second text, number_3=33)'


def test_set_empty_filters_dict_for_args():
    assert describe_call('ClassName', (1, 2, 3), {}, filters={}) == 'ClassName(1, 2, 3)'
    assert describe_call('ClassName', (1, 2), {}, filters={}) == 'ClassName(1, 2)'
    assert describe_call('ClassName', (1,), {}, filters={}) == 'ClassName(1)'

    assert describe_call('ClassName', ('lol', 'kek'), {}, filters={}) == "ClassName('lol', 'kek')"
    assert describe_call('ClassName', ('lol',), {}, filters={}) == "ClassName('lol')"

    assert describe_call('ClassName', ('lol', 1, 2, 3), {}, filters={}) == "ClassName('lol', 1, 2, 3)"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek'), {}, filters={}) == "ClassName('lol', 1, 2, 3, 'kek')"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, filters={}) == "ClassName('lol', 1, 2, 3, 'kek', None)"


def test_set_filters_dict_with_empty_lambdas_for_args():
    def allow_all(x):  # noqa: ARG001
        return True

    assert describe_call('ClassName', (1, 2, 3), {}, filters={0: allow_all, 1: allow_all, 2: allow_all}) == 'ClassName(1, 2, 3)'
    assert describe_call('ClassName', (1, 2), {}, filters={0: allow_all, 1: allow_all}) == 'ClassName(1, 2)'
    assert describe_call('ClassName', (1,), {}, filters={0: allow_all}) == 'ClassName(1)'

    assert describe_call('ClassName', ('lol', 'kek'), {}, filters={0: allow_all, 1: allow_all}) == "ClassName('lol', 'kek')"
    assert describe_call('ClassName', ('lol',), {}, filters={0: allow_all}) == "ClassName('lol')"

    assert describe_call('ClassName', ('lol', 1, 2, 3), {}, filters={0: allow_all, 1: allow_all, 2: allow_all}) == "ClassName('lol', 1, 2, 3)"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek'), {}, filters={0: allow_all, 1: allow_all, 2: allow_all, 3: allow_all}) == "ClassName('lol', 1, 2, 3, 'kek')"
    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, filters={0: allow_all, 1: allow_all, 2: allow_all, 3: allow_all, 4: allow_all}) == "ClassName('lol', 1, 2, 3, 'kek', None)"


def test_set_real_filters_for_args():
    def not_all(x):  # noqa: ARG001
        return False

    assert describe_call('ClassName', (1, 2, 3), {}, filters={0: not_all, 1: not_all, 2: not_all}) == 'ClassName()'
    assert describe_call('ClassName', (1,), {}, filters={0: not_all}) == 'ClassName()'
    assert describe_call('ClassName', ('lol', 'kek'), {}, filters={0: not_all, 1: not_all}) == "ClassName()"
    assert describe_call('ClassName', ('lol',), {}, filters={0: not_all}) == "ClassName()"

    assert describe_call('ClassName', (1, 2, 3), {}, filters={0: not_all}) == 'ClassName(2, 3)'
    assert describe_call('ClassName', (1, 2, 3), {}, filters={2: not_all}) == 'ClassName(1, 2)'
    assert describe_call('ClassName', (1, 2, 3), {}, filters={1: not_all}) == 'ClassName(1, 3)'
    assert describe_call('ClassName', (1, 2), {}, filters={0: not_all}) == 'ClassName(2)'
    assert describe_call('ClassName', (1, 2), {}, filters={1: not_all}) == 'ClassName(1)'
    assert describe_call('ClassName', (1, 2, 3), {}, filters={3: not_all}) == 'ClassName(1, 2, 3)'

    assert describe_call('ClassName', ('lol', 'kek'), {}, filters={0: not_all}) == "ClassName('kek')"
    assert describe_call('ClassName', ('lol', 'kek'), {}, filters={1: not_all}) == "ClassName('lol')"
    assert describe_call('ClassName', ('lol',), {}, filters={1: not_all}) == "ClassName('lol')"


def test_args_filters_are_getting_values():
    fields = []

    def add_to_fields(value: Any) -> bool:
        fields.append(value)
        return True

    assert describe_call('ClassName', ('lol', 1, 2, 3, 'kek', None), {}, filters={0: add_to_fields, 1: add_to_fields, 2: add_to_fields, 3: add_to_fields, 4: add_to_fields, 5: add_to_fields}) == "ClassName('lol', 1, 2, 3, 'kek', None)"

    assert fields == ['lol', 1, 2, 3, 'kek', None]


def test_kwargs_filters_are_getting_values():
    fields = []

    def add_to_fields(value: Any) -> bool:
        fields.append(value)
        return True

    assert describe_call('ClassName', (), {'lol': 'kek', 'kek': 'lol'}, filters={'lol': add_to_fields, 'kek': add_to_fields}) == "ClassName(lol='kek', kek='lol')"

    assert fields == ['kek', 'lol']


def test_set_empty_filters_dict_for_kwargs():
    assert describe_call('ClassName', (), {'lol': 1, 'kek': 2}, filters={}) == 'ClassName(lol=1, kek=2)'

    assert describe_call('ClassName', (), {'lol': 'insert text', 'kek': 'insert the second text'}, filters={}) == "ClassName(lol='insert text', kek='insert the second text')"

    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}, filters={}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}, filters={}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"


def test_set_filters_dict_with_empty_lambdas_for_kwargs():
    def allow_all(x):  # noqa: ARG001
        return True

    assert describe_call('ClassName', (), {'lol': 1, 'kek': 2}, filters={'lol': allow_all, 'kek': allow_all}) == 'ClassName(lol=1, kek=2)'

    assert describe_call('ClassName', (), {'lol': 'insert text', 'kek': 'insert the second text'}, filters={'lol': allow_all, 'kek': allow_all}) == "ClassName(lol='insert text', kek='insert the second text')"

    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text'}, filters={'lol': allow_all, 'kek': allow_all}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text')"
    assert describe_call('ClassName', (), {'number_1': 1, 'number_2': 2, 'lol': 'insert text', 'kek': 'insert the second text', 'number_3': 3}, filters={'lol': allow_all, 'kek': allow_all}) == "ClassName(number_1=1, number_2=2, lol='insert text', kek='insert the second text', number_3=3)"


def test_set_real_filters_for_kwargs():
    def not_all(x):  # noqa: ARG001
        return False

    assert describe_call('ClassName', (), {'lol': 1, 'kek': 2}, filters={'lol': not_all, 'kek': not_all}) == 'ClassName()'
    assert describe_call('ClassName', (), {'lol': 1, 'kek': 2}, filters={'lol': not_all}) == 'ClassName(kek=2)'
    assert describe_call('ClassName', (), {'lol': 1, 'kek': 2}, filters={'kek': not_all}) == 'ClassName(lol=1)'


def test_set_real_filters_for_args_and_kwargs():
    def not_all(x):  # noqa: ARG001
        return False

    assert describe_call('ClassName', (1, 2), {'lol': 1, 'kek': 2}, filters={'lol': not_all, 'kek': not_all, 0: not_all, 1: not_all}) == 'ClassName()'


def test_filter_not_nones():
    assert describe_call('ClassName', (1, 'lol', None), {'lol': 1, 'kek': None}, filters={'lol': not_none, 'kek': not_none, 0: not_none, 1: not_none, 2: not_none}) == "ClassName(1, 'lol', lol=1)"


def test_named_functions_as_arguments():
    def function():
        pass

    assert describe_call('ClassName', (1, 2, 3, function), {}) == 'ClassName(1, 2, 3, function)'
    assert describe_call('ClassName', (function,), {}) == 'ClassName(function)'
    assert describe_call('ClassName', (function,), {'function': function}) == 'ClassName(function, function=function)'
    assert describe_call('ClassName', (), {'function': function}) == 'ClassName(function=function)'
    assert describe_call('ClassName', (1, 2, 3, function), {'function': function}) == 'ClassName(1, 2, 3, function, function=function)'


def test_lambdas_as_arguments():
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {}) == 'ClassName(1, 2, 3, lambda x: x)'
    assert describe_call('ClassName', (lambda x: x,), {}) == 'ClassName(lambda x: x)'
    assert describe_call('ClassName', (lambda x: x,), {'function': lambda x: x}) == 'ClassName(λ, function=λ)'
    assert describe_call('ClassName', (), {'function': lambda x: x}) == 'ClassName(function=lambda x: x)'
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'function': lambda x: x}) == 'ClassName(1, 2, 3, λ, function=λ)'


def test_simple_placeholders():
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek'}, placeholders={}) == 'ClassName(1, 2, 3, lambda x: x, lol=\'kek\')'
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek'}, placeholders=None) == 'ClassName(1, 2, 3, lambda x: x, lol=\'kek\')'
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek'}, placeholders={'lol': '***'}) == 'ClassName(1, 2, 3, lambda x: x, lol=***)'
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '***'}) == 'ClassName(1, 2, 3, lambda x: x, lol=***, kek=\'lol\')'
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '***', 0: '***'}) == 'ClassName(***, 2, 3, lambda x: x, lol=***, kek=\'lol\')'
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '***', 0: '***', 3: '***'}) == 'ClassName(***, 2, 3, ***, lol=***, kek=\'lol\')'
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '***', 0: '***', 3: '***', 'kek': '&'}) == 'ClassName(***, 2, 3, ***, lol=***, kek=&)'
    assert describe_call('ClassName', (1, 2, 3, lambda x: x), {'lol': 'kek', 'kek': 'lol'}, placeholders={'lol': '🔒', 0: '***', 3: '***', 'kek': '&'}) == 'ClassName(***, 2, 3, ***, lol=🔒, kek=&)'


def test_wrong_serializator_callback():
    with pytest.raises(SignatureMismatchError):
        describe_call('ClassName', (1, 2, 3), {'lol': 'kek'}, serializer=lambda x, y: x + y)


def test_wrong_filter_callback():
    with pytest.raises(SignatureMismatchError):
        describe_call('ClassName', (), {'lol': 1, 'kek': 2}, filters={'kek': lambda x, y: x + y})

    with pytest.raises(SignatureMismatchError):
        describe_call('ClassName', (1, 2, 3), {}, filters={0: lambda x, y: x + y})


def test_print_classes():
    class SomeClass:
        pass

    assert describe_call('ClassName', (int, str, SomeClass), {'lol': int, 'kek': str, 'cheburek': SomeClass}) == 'ClassName(int, str, SomeClass, lol=int, kek=str, cheburek=SomeClass)'


def test_async_function_as_argument():
    async def function():
        pass

    assert describe_call('ClassName', (function,), {}) == 'ClassName(function)'
    assert describe_call('ClassName', (), {'function': function}) == 'ClassName(function=function)'


def test_broken_repr_as_argument():
    class BrokenRepr:
        def __repr__(self):
            raise RuntimeError("repr is broken")

    broken = BrokenRepr()
    assert describe_call('ClassName', (broken,), {}) == "ClassName(<BrokenRepr's object>)"
    assert describe_call('ClassName', (), {'x': broken}) == "ClassName(x=<BrokenRepr's object>)"
    assert describe_call('ClassName', (1, broken, 2), {'x': broken}) == "ClassName(1, <BrokenRepr's object>, 2, x=<BrokenRepr's object>)"


def test_item_limit_basic():
    """superrepr(12345) = '12345' (5 chars); item_limit=2 -> '12...'."""
    assert describe_call('C', (12345,), {}, item_limit=2) == 'C(12...)'
    assert describe_call('C', (), {'x': 12345}, item_limit=2) == 'C(x=12...)'


def test_item_limit_not_exceeded():
    """
    '12345' has 5 chars; item_limit=5 -> no truncation.

    item_limit=4 -> '1234...'.
    """
    assert describe_call('C', (12345,), {}, item_limit=5) == 'C(12345)'
    assert describe_call('C', (12345,), {}, item_limit=4) == 'C(1234...)'


def test_item_limit_zero():
    """item_limit=0 -> value fully replaced with '...'."""
    assert describe_call('C', (12345,), {}, item_limit=0) == 'C(...)'
    assert describe_call('C', (), {'x': 12345}, item_limit=0) == 'C(x=...)'


def test_item_limit_with_kwargs():
    """limit applies only to the value part, not to 'key=value' as a whole."""
    assert describe_call('C', (), {'key': 12345}, item_limit=2) == 'C(key=12...)'


def test_item_limit_negative():
    with pytest.raises(ValueError, match='item_limit must be a non-negative integer'):
        describe_call('C', (1,), {}, item_limit=-1)


def test_item_limit_with_placeholder():
    """item_limit applies to placeholder strings too."""
    assert describe_call('C', (1,), {}, item_limit=2, placeholders={0: 'secret'}) == 'C(se...)'


def test_item_limit_with_placeholder_not_exceeded():
    """placeholder shorter than item_limit — no truncation."""
    assert describe_call('C', (1,), {}, item_limit=10, placeholders={0: 'ok'}) == 'C(ok)'


def test_total_limit_basic():
    """
    'C(a=1, b=2, c=3)' = 16 chars; total_limit=10.

    content 'C(a=1, b=2)' = 11 > 10; content 'C(a=1)' = 7 <= 10 -> output 'C(a=1, ...)'.
    """
    assert describe_call('C', (), {'a': 1, 'b': 2, 'c': 3}, total_limit=10) == 'C(a=1, ...)'


def test_total_limit_not_exceeded():
    result = describe_call('C', (1, 2), {}, total_limit=100)
    assert result == 'C(1, 2)'
    assert len(result) <= 100


def test_total_limit_drops_to_ellipsis_only():
    """
    First item doesn't fit — result is ClassName(...).

    'Name(x=12345)' = 13 chars; total_limit=9 = minimum for 'Name' -> 'Name(...)'.
    """
    assert describe_call('Name', (), {'x': 12345}, total_limit=9) == 'Name(...)'


def test_total_limit_minimum():
    """Minimum is len(class_name) + 2; the actual output 'A(...)' may be longer."""
    name = 'A'
    minimum = len(name) + 2  # = 3
    result = describe_call(name, (1, 2, 3), {}, total_limit=minimum)

    assert result == 'A(...)'
    # Output is longer than total_limit because '...' marker doesn't count.
    assert len(result) > minimum


def test_total_limit_too_small():
    with pytest.raises(ValueError, match='total_limit'):
        describe_call('ClassName', (1,), {}, total_limit=5)


def test_total_limit_negative():
    with pytest.raises(ValueError, match='total_limit must be a non-negative integer'):
        describe_call('C', (1,), {}, total_limit=-1)


def test_total_limit_with_item_limit():
    """
    item_limit=2 truncates '12345' -> '12...', '1' stays as '1'.

    chunks: ['a=1', 'b=12...'] -> full: 'C(a=1, b=12...)' = 15 chars.
    total_limit=11: k=1 -> 'C(a=1, ...)' = 11 chars <= 11 ✓.
    """
    assert describe_call('C', (), {'a': 1, 'b': 12345}, item_limit=2, total_limit=11) == 'C(a=1, ...)'


def test_total_limit_first_item_too_long():
    """
    First and only item exceeds total_limit -> 'C(...)'.

    'C(a=12345)' = 10 chars; total_limit=6 = minimum -> 'C(...)'.
    """
    assert describe_call('C', (), {'a': 12345}, total_limit=6) == 'C(...)'


def test_total_limit_exact_fit():
    """'A(1, 2, 3)' = 10 chars; total_limit=10 -> no truncation."""
    result = describe_call('A', (1, 2, 3), {})
    assert result == 'A(1, 2, 3)'
    assert describe_call('A', (1, 2, 3), {}, total_limit=len(result)) == result


def test_item_limit_string_basic():
    """len('hello world') = 11 > 5; truncate to 5 raw chars -> repr('hello') + '...'."""
    assert describe_call('C', ('hello world',), {}, item_limit=5) == "C('hello'...)"
    assert describe_call('C', (), {'name': 'hello world'}, item_limit=5) == "C(name='hello'...)"


def test_item_limit_string_exact_boundary():
    """len('abc') = 3 == item_limit=3 -> no truncation."""
    assert describe_call('C', ('abc',), {}, item_limit=3) == "C('abc')"


def test_item_limit_string_one_over():
    """len('abcd') = 4 > item_limit=3 -> repr('abc') + '...'."""
    assert describe_call('C', ('abcd',), {}, item_limit=3) == "C('abc'...)"


def test_item_limit_string_zero():
    """item_limit=0: any non-empty string -> repr('') + '...' = "''" + '...'."""
    assert describe_call('C', ('abc',), {}, item_limit=0) == "C(''...)"


def test_item_limit_string_not_exceeded():
    """len('hi') = 2; item_limit=2 -> no truncation; item_limit=3 -> also no truncation."""
    assert describe_call('C', ('hi',), {}, item_limit=2) == "C('hi')"
    assert describe_call('C', ('hi',), {}, item_limit=3) == "C('hi')"


def test_item_limit_string_with_escape_chars():
    """'a\\nb' has len=3 ('\\n' is 1 raw char); item_limit=2 -> repr('a\\n') + '...'."""
    assert describe_call('C', ('a\nb',), {}, item_limit=2) == "C('a\\n'...)"


def test_item_limit_string_kwargs():
    """Truncation by raw length applies to kwargs values too."""
    assert describe_call('C', (), {'name': 'abcdef'}, item_limit=2) == "C(name='ab'...)"


def test_item_limit_string_custom_serializer():
    """Custom serializer: result doesn't equal repr(value), so generic truncation applies."""
    assert describe_call('C', ('hello',), {}, serializer=lambda x: str(x), item_limit=3) == 'C(hel...)'


def test_item_limit_bytes_basic():
    """len(b'hello world') = 11 > 5; truncate to 5 raw bytes -> repr(b'hello') + '...'."""
    assert describe_call('C', (b'hello world',), {}, item_limit=5) == "C(b'hello'...)"


def test_item_limit_bytes_exact_boundary():
    """len(b'abc') = 3 == item_limit=3 -> no truncation."""
    assert describe_call('C', (b'abc',), {}, item_limit=3) == "C(b'abc')"


def test_item_limit_bytes_one_over():
    """len(b'abcd') = 4 > item_limit=3 -> repr(b'abc') + '...'."""
    assert describe_call('C', (b'abcd',), {}, item_limit=3) == "C(b'abc'...)"


def test_item_limit_bytes_zero():
    """item_limit=0: any non-empty bytes -> repr(b'') + '...'."""
    assert describe_call('C', (b'abc',), {}, item_limit=0) == "C(b''...)"


def test_item_limit_bytes_with_non_ascii():
    """
    Non-ASCII bytes: repr uses escape sequences, but limit counts raw bytes.

    len(b'\\xff\\xfe') = 2; item_limit=1 -> repr(b'\\xff') + '...'.
    """
    assert describe_call('C', (b'\xff\xfe',), {}, item_limit=1) == "C(b'\\xff'...)"


def test_item_and_chunk_truncation_coexist():
    """
    item_limit truncates '123456' -> '12...'; total_limit then drops 'b=2' chunk.

    chunks after item_limit: ['a=12...', 'b=2']; full = 'S(a=12..., b=2)' = 15.
    total_limit=10: content 'S(a=12...)' = 10 <= 10 -> output 'S(a=12..., ...)'.
    """
    result = describe_call('S', (), {'a': 123456, 'b': 2}, item_limit=2, total_limit=10)
    assert result == 'S(a=12..., ...)'


def test_chunk_truncation_preserves_comma():
    """When k>0, output includes ', ...' (comma before ellipsis)."""
    result = describe_call('C', (), {'a': 1, 'b': 2}, total_limit=7)
    assert result == 'C(a=1, ...)'
    assert ', ...' in result


def test_chunk_truncation_no_comma_when_all_dropped():
    """When all chunks dropped (k==0), output is 'ClassName(...)' without comma."""
    result = describe_call('C', (), {'a': 12345}, total_limit=3)
    assert result == 'C(...)'
    assert ', ...' not in result


def test_item_limit_ellipsis_not_truncated():
    """Ellipsis value is never truncated by item_limit."""
    assert describe_call('C', (...,), {}, item_limit=1) == 'C(Ellipsis)'
    assert describe_call('C', (...,), {}, item_limit=0) == 'C(Ellipsis)'


def test_item_limit_ellipsis_with_placeholder():
    """Placeholder for Ellipsis is still subject to item_limit."""
    assert describe_call('C', (...,), {}, item_limit=2, placeholders={0: 'secret'}) == 'C(se...)'


def test_total_limit_output_longer_than_limit():
    """
    '...' marker doesn't count toward total_limit, so output can exceed total_limit.

    'C(a=1)' = 7 chars <= total_limit=7; output = 'C(a=1, ...)' = 11 > 7.
    """
    result = describe_call('C', (), {'a': 1, 'b': 2}, total_limit=7)
    assert result == 'C(a=1, ...)'
    assert len(result) > 7


def test_total_limit_ellipsis_not_dropped():
    """
    Ellipsis argument is never dropped by total_limit.

    'C(Ellipsis, x=1)' = 17 chars; small total_limit should drop 'x=1' but keep Ellipsis.
    """
    result = describe_call('C', (...,), {'x': 1}, total_limit=13)
    assert result == 'C(Ellipsis, ...)'


def test_total_limit_ellipsis_other_items_dropped():
    """
    Non-Ellipsis items are dropped before Ellipsis.

    'C(Ellipsis, 1, 2)' = 18 chars.
    Drop '2': content = 'C(Ellipsis, 1)' = 14 chars.
    Drop '1': content = 'C(Ellipsis)' = 11 chars.
    """
    result = describe_call('C', (..., 1, 2), {}, total_limit=11)
    assert result == 'C(Ellipsis, ...)'


def test_total_limit_all_ellipsis():
    """
    All arguments are Ellipsis — nothing can be dropped.

    Even if content exceeds total_limit, return full output (Ellipsis exemption).
    """
    result = describe_call('C', (..., ...), {}, total_limit=3)
    assert result == 'C(Ellipsis, Ellipsis)'


def test_total_limit_ellipsis_pinned_content_exceeds_limit():
    """
    Ellipsis + droppable item; even pinned-only content exceeds total_limit.

    'C(Ellipsis, 1)' = 14 > 3; drop '1': content 'C(Ellipsis)' = 11 > 3 -> fallback.
    Returns pinned-only + '...' regardless of limit.
    """
    result = describe_call('C', (..., 1), {}, total_limit=3)
    assert result == 'C(Ellipsis, ...)'


def test_total_limit_ellipsis_mixed_positions():
    """
    Ellipsis in the middle — order preserved, non-Ellipsis dropped from the end.

    'C(1, Ellipsis, 2)' = 18 chars.
    Drop '2': content = 'C(1, Ellipsis)' = 14 chars.
    """
    assert describe_call('C', (1, ..., 2), {}, total_limit=14) == 'C(1, Ellipsis, ...)'
