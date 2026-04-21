from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

from printo.reprs import superrepr


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
    if item_limit is not None:
        if placeholder is not None:
            if len(serialized) > item_limit:
                serialized = serialized[:item_limit] + '...'
        elif value is ...:
            pass  # Ellipsis is never truncated
        elif isinstance(value, (str, bytes)) and serialized == repr(value):
            if len(value) > item_limit:
                serialized = repr(value[:item_limit]) + '...'
        elif len(serialized) > item_limit:
            serialized = serialized[:item_limit] + '...'
    return serialized


def _serialize_items(  # noqa: PLR0913
    items: Iterable[Tuple[Union[str, int], Any]],
    format_chunk: Callable[[Union[str, int], str], str],
    filters: Dict[Union[str, int], Callable[[Any], bool]],
    get_placeholder: Callable[[Union[str, int]], Optional[str]],
    serializer: Callable[[Any], str],
    item_limit: Optional[int],
) -> Tuple[List[str], List[bool]]:
    chunks: List[str] = []
    pinned: List[bool] = []
    for key, value in items:
        result = _serialize_item(key, value, filters, get_placeholder, serializer, item_limit)
        if result is not None:
            chunks.append(format_chunk(key, result))
            pinned.append(value is ...)
    return chunks, pinned


def describe_call(  # noqa: PLR0913
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
        minimum = len(class_name) + 2
        if total_limit < minimum:
            raise ValueError(
                f'total_limit ({total_limit}) is too small for class name {class_name!r}. '
                f'Minimum is {minimum} (class name length + 2 for parentheses).',
            )

    real_filters: Dict[Union[str, int], Callable[[Any], bool]] = (
        filters if filters is not None else {}
    )
    get_placeholder: Callable[[Union[str, int]], Optional[str]] = lambda field_name: placeholders.get(field_name) if placeholders is not None else None

    args_chunks, args_pinned = _serialize_items(enumerate(args), lambda _, value: value, real_filters, get_placeholder, serializer, item_limit)
    kwargs_chunks, kwargs_pinned = _serialize_items(kwargs.items(), lambda key, value: f'{key}={value}', real_filters, get_placeholder, serializer, item_limit)

    all_chunks = args_chunks + kwargs_chunks
    all_pinned = args_pinned + kwargs_pinned

    full_output = f'{class_name}({", ".join(all_chunks)})'

    if total_limit is not None and len(full_output) > total_limit:
        droppable = [i for i in range(len(all_chunks)) if not all_pinned[i]]
        pinned_indices = [i for i in range(len(all_chunks)) if all_pinned[i]]

        for num_keep in range(len(droppable) - 1, -1, -1):
            kept_indices = sorted(pinned_indices + droppable[:num_keep])
            kept_chunks = [all_chunks[i] for i in kept_indices]
            if kept_chunks:
                content = f'{class_name}({", ".join(kept_chunks)})'
                output = f'{class_name}({", ".join(kept_chunks)}, ...)'
            else:
                content = f'{class_name}()'
                output = f'{class_name}(...)'
            if len(content) <= total_limit:
                return output

        # Ellipsis exemption: all droppable dropped, return pinned-only output regardless of limit
        pinned_chunks = [all_chunks[i] for i in pinned_indices]
        if not droppable:
            return full_output
        return f'{class_name}({", ".join(pinned_chunks)}, ...)'

    return full_output


descript_data_object = describe_call
describe_data_object = describe_call
