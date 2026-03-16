from ast import Assign, Attribute, Name, parse
from functools import partial
from inspect import Parameter, Signature, getattr_static, isclass, signature
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from getsources import getclearsource

from printo import describe_data_object
from printo.errors import (
    CanNotBePositionalError,
    ParameterMappingNotFoundError,
    RedefinitionError,
)

ClassType = TypeVar('ClassType', bound=Type[Any])

def get_mapping(cls: ClassType) -> Dict[str, str]:
    try:
        source = getclearsource(cls.__init__)
    except TypeError:
        return {}

    tree = parse(source)

    try:
        self_name = tree.body[0].args.posonlyargs[0].arg  # type: ignore[attr-defined]
    except IndexError:
        try:
            self_name = tree.body[0].args.args[0].arg  # type: ignore[attr-defined]
        except IndexError as e:
            raise ParameterMappingNotFoundError(f'It seems that the "self" argument was not found for the __init__ method of class {cls.__name__}.') from e

    results = {}
    for node in tree.body[0].body:  # type: ignore[attr-defined]
        if isinstance(node, Assign) and len(node.targets) == 1 and isinstance(node.targets[0], Attribute) and isinstance(node.targets[0].value, Name) and node.targets[0].value.id == self_name and isinstance(node.value, Name):
            results[node.value.id] = node.targets[0].attr

    return results

def repred(cls: Optional[ClassType] = None, prefer_positional: bool = False, qualname: bool = False, getters: Optional[Dict[str, Callable[[ClassType], Any]]] = None, filters: Optional[Dict[Union[str, int], Callable[[Any], bool]]] = None, ignore: Optional[List[str]] = None, positionals: Optional[List[str]] = None) -> Union[ClassType, Callable[[ClassType], ClassType]]:  # noqa: PLR0915, PLR0913
    from sigmatch import (  # noqa: PLC0415
        PossibleCallMatcher,
        SignatureMismatchError,
    )

    if cls is None:
        return partial(repred, prefer_positional=prefer_positional, qualname=qualname, getters=getters, filters=filters, ignore=ignore, positionals=positionals)  # type: ignore[return-value]

    if not isclass(cls):
        raise ValueError('The @repred decorator can only be applied to classes.')
    if '__repr__' in cls.__dict__:
        raise RedefinitionError(f'Class {cls.__name__} already has its own __repr__ method defined; you cannot override it.')
    if getters is not None:
        matcher = PossibleCallMatcher('.')
        for parameter_name, getter in getters.items():
            if not matcher.match(getter):
                raise SignatureMismatchError(f'You have defined a getter for parameter "{parameter_name}" that cannot be called with a single argument (an object of class {cls.__name__}).')
        default_getters = getters
    else:
        default_getters = {}

    if filters is not None:
        matcher = PossibleCallMatcher('.')
        for parameter_name_or_id, filter_function in filters.items():
            if not isinstance(parameter_name_or_id, (int, str)) or (isinstance(parameter_name_or_id, int) and parameter_name_or_id < 0) or (isinstance(parameter_name_or_id, str) and not parameter_name_or_id.isidentifier()):
                raise ValueError('Keys for a filtered dictionary can be either integers starting from 0 or strings (parameter names).')
            if not matcher.match(filter_function):
                raise SignatureMismatchError(f'You have defined a getter for parameter "{parameter_name_or_id}" that cannot be called with a single argument.')
    else:
        filters = {}

    if ignore is not None:
        for parameter_name in ignore:
            if not parameter_name.isidentifier():
                raise ValueError(f'You have specified the parameter name {parameter_name!r} to ignore, which is not a valid identifier name in Python.')
    else:
        ignore = []
    ignored_parameters = set(ignore)

    if positionals:
        for parameter_name in positionals:
            if not parameter_name.isidentifier():
                raise ValueError(f'You have specified the parameter name {parameter_name!r} as a positional, which is not a valid identifier name in Python.')
    else:
        positionals = []
    positionals_to_compare = set(positionals)

    names_mapping = get_mapping(cls)

    positional_getters = {}
    keyword_getters = {}
    default_values = {}
    one_star_parameter = None
    two_stars_parameter = None
    all_parameter_names = set()
    parameters_not_found = []

    init_signature: Optional[Signature] = signature(cls.__init__)

    if getattr_static(cls, '__init__') is not object.__init__:
        parameters: Iterable[Parameter] = cast(Signature, init_signature).parameters.values()
    else:
        parameters = []

    for position, parameter in enumerate(parameters):
        parameter_name = parameter.name
        if position and parameter_name not in ignored_parameters:
            if parameter.kind == Parameter.VAR_POSITIONAL:
                one_star_parameter = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
            elif parameter.kind == Parameter.VAR_KEYWORD:
                if parameter_name in positionals_to_compare:
                    raise CanNotBePositionalError(f'Parameter {parameter_name} cannot be represented as a positional one.')
                two_stars_parameter = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)

    counted_as_keywords = 0

    for position, parameter in enumerate(parameters):
        if position:
            parameter_name = parameter.name

            all_parameter_names.add(parameter_name)

            if parameter_name not in names_mapping and parameter_name not in default_getters and parameter.default == parameter.empty and parameter_name not in ignored_parameters:
                parameters_not_found.append(parameter_name)

            if parameter_name not in ignored_parameters:
                if parameter.kind == Parameter.POSITIONAL_ONLY:
                    positional_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
                elif parameter.kind == Parameter.KEYWORD_ONLY:
                    if parameter_name in positionals_to_compare:
                        raise CanNotBePositionalError(f'Parameter {parameter_name} cannot be represented as a positional one.')
                    keyword_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
                elif parameter.kind == Parameter.POSITIONAL_OR_KEYWORD:
                    if parameter_name in positionals_to_compare and counted_as_keywords:
                        raise CanNotBePositionalError(f'Parameter {parameter_name} cannot be represented as a positional one.')
                    if prefer_positional or one_star_parameter is not None or parameter_name in positionals_to_compare:
                        positional_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
                    else:
                        counted_as_keywords += 1
                        keyword_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)

                if parameter.default != parameter.empty:
                    default_values[parameter_name] = parameter.default

    for parameter_name in default_getters:
        if parameter_name not in all_parameter_names:
            raise NameError(f'Parameter "{parameter_name}" is not used when initializing objects of class {cls.__name__}, but you have defined a getter for it.')

    for parameter_name in ignored_parameters:
        if parameter_name not in all_parameter_names:
            raise NameError(f'Parameter "{parameter_name}" is not used when initializing objects of class {cls.__name__}, but you have defined it as an ignored one.')

    for parameter_name in positionals_to_compare:
        if parameter_name not in all_parameter_names:
            raise NameError(f'Parameter "{parameter_name}" is not used when initializing objects of class {cls.__name__}, but you have defined it as a position one.')

    if parameters_not_found:
        raise ParameterMappingNotFoundError(f'No internal object {"properties" if len(parameters_not_found) > 1 else "property"} or custom {"getters" if len(parameters_not_found) > 1 else "getter"} {"were" if len(parameters_not_found) > 1 else "was"} found for the {"parameters" if len(parameters_not_found) > 1 else "parameter"} {", ".join(parameters_not_found)}.')

    def __repr__(self: ClassType) -> str:  # noqa: N807
        positionals = []
        for name, getter in positional_getters.items():
            value = default_getters[name](self) if name in default_getters else getter(self)
            if not (name in default_values and default_values[name] is value):
                positionals.append(value)

        keywords = {}
        for name, getter in keyword_getters.items():
            value = default_getters[name](self) if name in default_getters else getter(self)
            if name not in default_values or default_values[name] is not value:
                keywords[name] = value

        if one_star_parameter is not None:
            positionals += list(one_star_parameter(self))
        if two_stars_parameter is not None:
            keywords.update(two_stars_parameter(self))

        class_name = cls.__qualname__ if qualname else cls.__name__

        return describe_data_object(
            class_name,
            positionals,
            keywords,
            filters=filters,
        )

    cls.__repr__ = __repr__  # type: ignore[assignment]

    return cls
