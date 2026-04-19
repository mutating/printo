from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

from printo.reprs import superrepr


def describe_data_object(  # noqa: PLR0913
    class_name: str,
    args: Union[Tuple[Any, ...], List[Any]],
    kwargs: Dict[str, Any],
    serializer: Callable[[Any], str] = superrepr,
    filters: Optional[Dict[Union[str, int], Callable[[Any], bool]]] = None,
    placeholders: Optional[Dict[Union[str, int], str]] = None,
) -> str:
    from sigmatch import PossibleCallMatcher  # noqa: PLC0415

    PossibleCallMatcher('.').match(serializer, raise_exception=True)

    real_filters: Dict[Union[str, int], Callable[[Any], bool]] = (
        filters if filters is not None else {}
    )
    get_placeholder: Callable[[Union[str, int]], Optional[str]] = lambda field_name: placeholders.get(field_name) if placeholders is not None else None

    def serialize_item(
        key: Union[str, int],
        value: Any,
    ) -> Optional[str]:
        decider = real_filters.get(key, lambda x: True)  # noqa: ARG005
        PossibleCallMatcher('.').match(decider, raise_exception=True)
        if not decider(value):
            return None
        placeholder = get_placeholder(key)
        return placeholder if placeholder is not None else serializer(value)

    def serialize_items(
        items: Iterable[Tuple[Union[str, int], Any]],
        format_chunk: Callable[[Union[str, int], str], str],
    ) -> str:
        chunks = []
        for key, value in items:
            result = serialize_item(key, value)
            if result is not None:
                chunks.append(format_chunk(key, result))
        return ', '.join(chunks)

    args_description = serialize_items(enumerate(args), lambda _, value: value)
    kwargs_description = serialize_items(kwargs.items(), lambda key, value: f'{key}={value}')

    breackets_content = ', '.join(
        [x for x in (args_description, kwargs_description) if x],
    )

    return f'{class_name}({breackets_content})'


descript_data_object = describe_data_object
