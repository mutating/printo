from typing import Type, Any, TypeVar, Dict, Optional, cast
from inspect import getattr_static, isclass, signature, Signature, Parameter
from ast import parse, walk, Assign, Attribute, Name
from functools import partial

from printo.errors import RedefinitionError, ParameterMappingNotFoundError
from printo import describe_data_object
from getsources import getclearsource


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


def repred(cls: ClassType) -> ClassType:
    if not isclass(cls):
        raise ValueError()
    if getattr_static(cls, '__repr__') is not object.__repr__:
        raise RedefinitionError(f'Class {cls.__name__} already has its own __repr__ method defined; you cannot override it.')

    names_mapping = get_mapping(cls)

    positional_getters = {}
    keyword_getters = {}
    defaults = {}
    one_star_parameter = None
    two_stars_parameter = None

    init_signature: Optional[Signature] = signature(cls.__init__)

    for position, parameter in enumerate(cast(Signature, init_signature).parameters.values()):
        if position:
            parameter_name = parameter.name
            if parameter_name not in names_mapping and parameter.default == parameter.empty:
                raise ParameterMappingNotFoundError()

            if parameter.kind == Parameter.POSITIONAL_ONLY:
                positional_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
            elif parameter.kind == Parameter.POSITIONAL_OR_KEYWORD or parameter.kind == Parameter.KEYWORD_ONLY:
                keyword_getters[parameter_name] = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
            elif parameter.kind == Parameter.VAR_POSITIONAL:
                one_star_parameter = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)
            elif parameter.kind == Parameter.VAR_KEYWORD:
                two_stars_parameter = partial((lambda key, object_of_this_class: getattr(object_of_this_class, names_mapping[key])), parameter_name)

            if parameter.default != parameter.empty:
                defaults[parameter_name] = parameter.default

    def __repr__(self) -> str:
        positionals = []
        for name, getter in positional_getters.items():
            value = getter(self)
            if not (name in defaults and defaults[name] is value):
                positionals.append(value)

        keywords = {}
        for name, getter in keyword_getters.items():
            value = getter(self)
            if name not in defaults or defaults[name] is not value:
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
