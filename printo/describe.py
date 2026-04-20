from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

from printo.reprs import superrepr


def _truncate_string_repr(value: str, item_limit: int) -> str:
    if len(repr('')) > item_limit:
        return repr(value)[:item_limit] + '...'
    lo, hi = 0, len(value)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if len(repr(value[:mid])) <= item_limit:
            lo = mid
        else:
            hi = mid - 1
    return repr(value[:lo]) + '...'


def _serialize_item(  # noqa: PLR0913
    key: Union[str, int],
    value: Any,
    filters: Dict[Union[str, int], Callable[[Any], bool]],
    get_placeholder: Callable[[Union[str, int]], Optional[str]],
    serializer: Callable[[Any], str],
    item_limit: Optional[int],
) -> Optional[str]:
    from sigmatch import PossibleCallMatcher  # noqa: PLC0415

    decider = filters.get(key, lambda x: True)  # noqa: ARG005
    PossibleCallMatcher('.').match(decider, raise_exception=True)
    if not decider(value):
        return None
    placeholder = get_placeholder(key)
    serialized = placeholder if placeholder is not None else serializer(value)
    if item_limit is not None and len(serialized) > item_limit:
        if placeholder is None and isinstance(value, str) and serialized == repr(value):
            serialized = _truncate_string_repr(value, item_limit)
        else:
            serialized = serialized[:item_limit] + '...'
    return serialized


def _serialize_items(  # noqa: PLR0913
    items: Iterable[Tuple[Union[str, int], Any]],
    format_chunk: Callable[[Union[str, int], str], str],
    filters: Dict[Union[str, int], Callable[[Any], bool]],
    get_placeholder: Callable[[Union[str, int]], Optional[str]],
    serializer: Callable[[Any], str],
    item_limit: Optional[int],
) -> List[str]:
    chunks = []
    for key, value in items:
        result = _serialize_item(key, value, filters, get_placeholder, serializer, item_limit)
        if result is not None:
            chunks.append(format_chunk(key, result))
    return chunks


def describe_data_object(  # noqa: PLR0913
    class_name: str,
    args: Union[Tuple[Any, ...], List[Any]],
    kwargs: Dict[str, Any],
    serializer: Callable[[Any], str] = superrepr,
    filters: Optional[Dict[Union[str, int], Callable[[Any], bool]]] = None,
    placeholders: Optional[Dict[Union[str, int], str]] = None,
    item_limit: Optional[int] = None,
    total_limit: Optional[int] = None,
) -> str:
    from sigmatch import PossibleCallMatcher  # noqa: PLC0415

    PossibleCallMatcher('.').match(serializer, raise_exception=True)

    if item_limit is not None and item_limit < 0:
        raise ValueError(f'item_limit must be a non-negative integer, got {item_limit}.')

    if total_limit is not None:
        if total_limit < 0:
            raise ValueError(f'total_limit must be a non-negative integer, got {total_limit}.')
        minimum = len(class_name) + 5
        if total_limit < minimum:
            raise ValueError(
                f'total_limit ({total_limit}) is too small for class name {class_name!r}. '
                f'Minimum is {minimum} (class name length + 5 for parentheses and ellipsis).',
            )

    real_filters: Dict[Union[str, int], Callable[[Any], bool]] = (
        filters if filters is not None else {}
    )
    get_placeholder: Callable[[Union[str, int]], Optional[str]] = lambda field_name: placeholders.get(field_name) if placeholders is not None else None

    args_chunks = _serialize_items(enumerate(args), lambda _, value: value, real_filters, get_placeholder, serializer, item_limit)
    kwargs_chunks = _serialize_items(kwargs.items(), lambda key, value: f'{key}={value}', real_filters, get_placeholder, serializer, item_limit)

    all_chunks = args_chunks + kwargs_chunks

    full_output = f'{class_name}({", ".join(all_chunks)})'

    if total_limit is not None and len(full_output) > total_limit:
        for k in range(len(all_chunks) - 1, -1, -1):
            if k == 0:
                candidate = f'{class_name}(...)'
            else:
                candidate = f'{class_name}({", ".join(all_chunks[:k])}, ...)'
            if len(candidate) <= total_limit:
                return candidate

    return full_output


descript_data_object = describe_data_object
