<details>
  <summary>ⓘ</summary>

[![Downloads](https://static.pepy.tech/badge/printo/month)](https://pepy.tech/project/printo)
[![Downloads](https://static.pepy.tech/badge/printo)](https://pepy.tech/project/printo)
[![Coverage Status](https://coveralls.io/repos/github/mutating/printo/badge.svg?branch=main)](https://coveralls.io/github/mutating/printo?branch=main)
[![Lines of code](https://sloc.xyz/github/mutating/printo/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/mutating/printo?branch=main)](https://hitsofcode.com/github/mutating/printo/view?branch=main)
[![Test-Package](https://github.com/mutating/printo/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/mutating/printo/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/printo.svg)](https://pypi.python.org/pypi/printo)
[![PyPI version](https://badge.fury.io/py/printo.svg)](https://badge.fury.io/py/printo)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/mutating/printo)

</details>

![logo](https://raw.githubusercontent.com/mutating/printo/develop/docs/assets/logo_1.svg)


Pythonistas follow an implicit convention to create special [`__repr__`](https://docs.python.org/3/reference/datamodel.html#object.__repr__) methods that return text closely resembling the code used to construct the object. With this library, you can easily implement `__repr__` for your own classes to follow this convention.


## Table of contents

- [**Installation**](#installation)
- [**Basic usage**](#basic-usage)
- [**Filtering**](#filtering)
- [**Custom display of objects**](#custom-display-of-objects)
- [**Placeholders**](#placeholders)
- [**Auto mode**](#auto-mode)


## Installation

You can install [`printo`](https://pypi.org/project/printo) with `pip`:

```bash
pip install printo
```

You can also use [`instld`](https://github.com/pomponchik/instld) to quickly try this package and others without installing them.


## Basic usage

The main function in this library is `describe_data_object`; it returns a string representing the initialization code for your object. There are three required positional parameters:

- A class name.
- A `list` or `tuple` of positional arguments.
- A `dict` of keyword arguments, where the keys are the names of the arguments, and the values are arbitrary objects.

Here's a simple example of how it works:

```python
from printo import describe_data_object

print(
    describe_data_object(
        'MyClassName',
        (1, 2, 'some text'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
    )
)
#> MyClassName(1, 2, 'some text', variable_name=1, second_variable_name='kek')
```


## Filtering

You can prevent individual parameters from being displayed. To do this, pass a `dict` to the `filters` parameter. The keys identify arguments by index or name. The values are functions that return a `bool` — `True` keeps the argument and `False` skips it:

```python
print(
    describe_data_object(
        'MyClassName',
        (1, 2, 'some text'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
        filters={1: lambda x: False if x == 2 else True, 'second_variable_name': lambda x: False},
    )
)
#> MyClassName(1, 'some text', variable_name=1)
```

You can also use the provided `not_none` filter to automatically exclude `None` values:

```python
from printo import not_none

print(
    describe_data_object(
        'MyClassName',
        (1, None),
        {},
        filters={1: not_none},
    )
)
#> MyClassName(1)
```


## Custom display of objects

By default, all argument values are represented in the same way as the standard [`repr`](https://docs.python.org/3/library/functions.html#repr) function would show them. There are only three exceptions:

- For regular functions, the function name is displayed.
- For classes, the class name is displayed.
- For lambda functions, the complete source code is displayed. However, if a single line of source code contains more than one lambda function, only the `λ` symbol is displayed (this is a technical limitation of source code reflection in Python).

You can provide a custom serialization function for each argument value via the `serializer` parameter:

```python
print(
    describe_data_object(
        'MyClassName',
        (1, 2, 'lol'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
        serializer=lambda x: repr(x * 2),
    )
)
#> MyClassName(2, 4, 'lollol', variable_name=2, second_variable_name='kekkek')
```


## Placeholders

For individual parameters, you can pass arbitrary strings that will be displayed instead of the actual values. This can be useful, for example, to hide the values of sensitive fields when serializing objects.

Pass a `dict` to the `placeholders` parameter, where the keys are argument names (for keyword arguments) or indices (for positional parameters, zero-indexed), and the values are strings:

```python
print(
    describe_data_object(
        'MySuperClass',
        (1, 2, 'lol'),
        {'variable_name': 1, 'second_variable_name': 'kek'},
        placeholders={
            1: '***',
            'variable_name': '***',
        },
    )
)
#> MySuperClass(1, ***, 'lol', variable_name=***, second_variable_name='kek')
```

> 🤓 If you set a placeholder for a parameter, the [custom serializer](#custom-display-of-objects) will not be applied to it.


## Auto mode

You can remove the boilerplate code by using the `@repred` decorator for your class:

```python
from printo import repred

@repred
class SomeClass:
    def __init__(self, a, b, c, *args, **kwargs):
        self.a = a
        self.b = b
        self.c = c
        self.args = args
        self.kwargs = kwargs

print(SomeClass(1, 2, 3))
#> SomeClass(1, 2, 3)
print(SomeClass(1, 2, 3, 4, 5))
#> SomeClass(1, 2, 3, 4, 5)
print(SomeClass(1, 2, 3, 4, 5, d=lambda x: x))
#> SomeClass(1, 2, 3, 4, 5, d=lambda x: x)
```

How does it work? Behind the scenes, the decorator uses AST analysis to generate code. The decorator attempts to determine which arguments passed to `__init__` are stored in which attributes. In other words, it looks for direct assignments of the form `self.a = a` in the `__init__` method.

If there is no *direct assignment* of a specific argument, an exception will be raised:

```python
@repred
class SomeClass:
    def __init__(self, a):
        ...

#> ...
#> printo.errors.ParameterMappingNotFoundError: No internal object property or custom getter was found for the parameter a.
```

> ↑ The error occurs when the class is decorated.

If, for some reason, you are unable to specify this mapping in the body of the `__init__` method, you can pass a function for a specific parameter that will extract it:

```python
@repred(getters={'a': lambda x: x.a})
class SomeClass:
    def __init__(self, a):
        self.a = self.convert_a(a)

    def convert_a(self, a):
        return a

print(SomeClass(123))
#> SomeClass(a=123)
```

By default, `@repred` displays all arguments as keywords in most cases. However, you can pass the `prefer_positional` argument to the decorator, which will cause it to prefer omitting argument names in such cases:

```python
@repred
class Class1:
    def __init__(self, a, b):
        self.a = a
        self.b = b

@repred(prefer_positional=True)
class Class2:
    def __init__(self, a, b):
        self.a = a
        self.b = b

print(Class1(123, 456))
#> Class1(a=123, b=456)
print(Class2(123, 456))
#> Class2(123, 456)
```

You can also choose to display only certain parameters as positional:

```python
@repred(positionals=['a'])
class SomeClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

print(SomeClass(123, 456))
#> SomeClass(123, b=456)
```

If you want to prevent certain `__init__` parameters from being displayed, you can add their names to the ignore list:

```python
@repred(ignore=['a'])
class SomeClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

print(SomeClass(123, 456))
#> SomeClass(b=456)
```

You can also add value-based filters for individual arguments by passing a `dict` of filters, similar to how it works in [manual mode](#filtering):

```python
from printo import not_none

@repred(filters={'a': not_none})
class SomeClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

print(SomeClass(None, None))
#> SomeClass(b=None)
print(SomeClass(123, 456))
#> SomeClass(a=123, b=456)
```

By default, the class name is displayed based on its `__name__` attribute, but you can configure it to use the `__qualname__` attribute instead:

```python
def function():
    @repred(qualname=True)
    class SomeClass:
        def __init__(self, a, b):
            self.a = a
            self.b = b
    return SomeClass

print(function()(123, 456))
#> function.<locals>.SomeClass(a=123, b=456)
```

> ⚠️ Auto mode is currently experimental, so there may be some bugs.
