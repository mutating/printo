from ast import Assign, Attribute, Name, parse
from functools import partial
from inspect import Parameter, Signature, getattr_static, isclass, signature
from typing import Any, Dict, Optional, Type, TypeVar, Callable, cast

from getsources import getclearsource

from printo import describe_data_object
from printo.errors import ParameterMappingNotFoundError, RedefinitionError

ClassType = TypeVar('ClassType', bound=Type[Any])

def get_mapping(cls: ClassType) -> Dict[str, str]:
    try:
        source = getclearsource(cls.__init__)
    except TypeError:
        return {}

    tree = parse(source)

    self_name = tree.body[0].args.args[0].arg

    results = {}
    for node in tree.body[0].body:
        if isinstance(node, Assign) and len(node.targets) == 1 and isinstance(node.targets[0], Attribute) and isinstance(node.targets[0].value, Name) and node.targets[0].value.id == self_name and isinstance(node.value, Name):
            results[node.value.id] = node.targets[0].attr

    return results

def repred(cls: Optional[ClassType] = None, prefer_positional: bool = False, getters: Optional[Dict[str, Callable[[ClassType], Any]]] = None) -> ClassType:
    if cls is None:
        return partial(repred, prefer_positional=prefer_positional, getters=getters)

    if not isclass(cls):
        raise ValueError('The @repred decorator can only be applied to classes.')
    if '__repr__' in cls.__dict__:
        raise RedefinitionError(f'Class {cls.__name__} already has its own __repr__ method defined; you cannot override it.')
    if getters is not None:
        from sigmatch import PossibleCallMatcher, SignatureMismatchError  # noqa: PLC0415

        matcher = PossibleCallMatcher('.')
        for parameter_name, getter in getters.items():
            if not matcher.match(getter):
                raise SignatureMismatchError(f'You have defined a getter for parameter "{parameter_name}" that cannot be called with a single argument (an object of class {cls.__name__}).')

        default_getters = getters
    else:
        default_getters = {}

    names_mapping = get_mapping(cls)

    positional_getters = {}
    keyword_getters = {}
    default_values = {}
    one_star_parameter = None
    two_stars_parameter = None

    init_signature: Optional[Signature] = signature(cls.__init__)

    if getattr_static(cls, '__init__') is not object.__init__:
        parameters = cast(Signature, init_signature).parameters.values()
    else:
        parameters = []

    for position, parameter in enumerate(parameters):
        if position:
            parameter_name = parameter.name
            if parameter_name not in names_mapping and parameter_name not in default_getters and parameter.default == parameter.empty:
                raise ParameterMappingNotFoundError()

            if parameter.kind == Parameter.POSITIONAL_ONLY:
                positional_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
            elif parameter.kind == Parameter.KEYWORD_ONLY:
                keyword_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
            elif parameter.kind == Parameter.POSITIONAL_OR_KEYWORD:
                if prefer_positional:
                    positional_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
                else:
                    keyword_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
            elif parameter.kind == Parameter.VAR_POSITIONAL:
                one_star_parameter = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
            elif parameter.kind == Parameter.VAR_KEYWORD:
                two_stars_parameter = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)

            if parameter.default != parameter.empty:
                default_values[parameter_name] = parameter.default

    def __repr__(self) -> str:  # noqa: N807
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

        return describe_data_object(
            cls.__name__,
            positionals,
            keywords,
        )

    cls.__repr__ = __repr__

    return cls
