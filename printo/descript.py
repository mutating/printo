from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from printo.reprs import superrepr


def descript_data_object(  # noqa: PLR0913
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

    args_description_chunks = []
    for index, argument in enumerate(args):
        decider = real_filters.get(index, lambda x: True)  # noqa: ARG005
        if decider(argument):
            placeholder = get_placeholder(index)
            if placeholder is not None:
                serialized_value = placeholder
            else:
                serialized_value = serializer(argument)
            args_description_chunks.append(serialized_value)
    args_description: str = ', '.join(args_description_chunks)

    kwargs_description_chunks = []
    for argument_name, value in kwargs.items():
        decider = real_filters.get(argument_name, lambda x: True)  # noqa: ARG005
        PossibleCallMatcher('.').match(decider, raise_exception=True)
        if decider(value):
            placeholder = get_placeholder(argument_name)
            if placeholder is not None:
                serialized_value = placeholder
            else:
                serialized_value = serializer(value)
            kwargs_description_chunks.append(f'{argument_name}=' + serialized_value)
    kwargs_description: str = ', '.join(kwargs_description_chunks)

    breackets_content = ', '.join(
        [x for x in (args_description, kwargs_description) if x],
    )

    return f'{class_name}({breackets_content})'
