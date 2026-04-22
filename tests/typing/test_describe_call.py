import pytest
from full_match import match

from printo import describe_call, not_none


@pytest.mark.mypy_testing
def test_describe_call_basic():
    """mypy accepts the basic call signature and infers str return type."""
    _: str = describe_call('MyClass', (1, 2, 'text'), {'key': 1})


@pytest.mark.mypy_testing
def test_describe_call_with_list_args():
    """mypy accepts a list for the args parameter, not only tuple."""
    _: str = describe_call('MyClass', [1, 2, 'text'], {'key': 1})


@pytest.mark.mypy_testing
def test_describe_call_with_filters():
    """mypy accepts a filters dict with int and str keys and callable values."""
    _: str = describe_call('MyClass', (1, 2), {'key': 1}, filters={1: lambda x: x != 2, 'key': lambda _: True})


@pytest.mark.mypy_testing
def test_describe_call_with_not_none_filter():
    """mypy accepts not_none as a valid filter value."""
    _: str = describe_call('MyClass', (1, None), {}, filters={1: not_none})


@pytest.mark.mypy_testing
def test_describe_call_with_serializer():
    """mypy accepts a Callable[[Any], str] for the serializer parameter."""
    _: str = describe_call('MyClass', (1, 2), {'key': 'val'}, serializer=lambda x: repr(x).upper())


@pytest.mark.mypy_testing
def test_describe_call_with_placeholders():
    """mypy accepts a placeholders dict with str and int keys and str values."""
    _: str = describe_call('MyClass', (1, 2), {'password': 'secret'}, placeholders={0: '***', 'password': '***'})


@pytest.mark.mypy_testing
def test_describe_call_with_item_limit():
    """mypy accepts an int for the item_limit parameter."""
    _: str = describe_call('MyClass', (123456789,), {'name': 'a very long string'}, item_limit=5)


@pytest.mark.mypy_testing
def test_describe_call_with_total_limit():
    """mypy accepts an int for the total_limit parameter."""
    _: str = describe_call('MyClass', (), {'a': 1, 'b': 2, 'c': 3}, total_limit=20)


@pytest.mark.mypy_testing
def test_describe_call_invalid_class_name_type():
    """mypy rejects int as class_name — expected str."""
    describe_call(42, [], {})  # E: [arg-type]


@pytest.mark.mypy_testing
def test_describe_call_invalid_args_type():
    """mypy rejects dict as args — expected Tuple or List."""
    describe_call('MyClass', {}, {})  # E: [arg-type]


@pytest.mark.mypy_testing
def test_describe_call_invalid_kwargs_key_type():
    """mypy rejects int as a kwargs key — expected str."""
    describe_call('MyClass', (), {1: 'val'})  # E: [dict-item]


@pytest.mark.mypy_testing
def test_describe_call_invalid_kwargs_type():
    """mypy rejects list as kwargs — expected Dict[str, Any]."""
    with pytest.raises(AttributeError, match=match("'list' object has no attribute 'items'")):
        describe_call('MyClass', [], [])  # E: [arg-type]


@pytest.mark.mypy_testing
def test_describe_call_invalid_serializer_type():
    """mypy rejects int as serializer — expected Callable[[Any], str]."""
    with pytest.raises(ValueError, match=match('It is impossible to determine the signature of an object that is not being callable.')):
        describe_call('MyClass', [], {}, serializer=42)  # E: [arg-type]


@pytest.mark.mypy_testing
def test_describe_call_invalid_filters_key_type():
    """mypy rejects float as a filters key — expected str or int."""
    describe_call('MyClass', [], {}, filters={1.5: not_none})  # E: [dict-item]


@pytest.mark.mypy_testing
def test_describe_call_invalid_filters_value_type():
    """mypy rejects int as a filters value — expected Callable[[Any], bool]."""
    describe_call('MyClass', [], {}, filters={'x': 42})  # E: [dict-item]


@pytest.mark.mypy_testing
def test_describe_call_invalid_placeholders_key_type():
    """mypy rejects float as a placeholders key — expected str or int."""
    describe_call('MyClass', [], {}, placeholders={1.5: '***'})  # E: [dict-item]


@pytest.mark.mypy_testing
def test_describe_call_invalid_placeholders_value_type():
    """mypy rejects int as a placeholders value — expected str."""
    describe_call('MyClass', [], {}, placeholders={'x': 42})  # E: [dict-item]


@pytest.mark.mypy_testing
def test_describe_call_invalid_item_limit_type():
    """mypy rejects str as item_limit — expected int."""
    with pytest.raises(TypeError, match=match("'<' not supported between instances of 'str' and 'int'")):
        describe_call('MyClass', [], {}, item_limit='5')  # E: [arg-type]


@pytest.mark.mypy_testing
def test_describe_call_invalid_total_limit_type():
    """mypy rejects str as total_limit — expected int."""
    with pytest.raises(TypeError, match=match("'<' not supported between instances of 'str' and 'int'")):
        describe_call('MyClass', [], {}, total_limit='15')  # E: [arg-type]
