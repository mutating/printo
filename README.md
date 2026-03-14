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


There is an implicit agreement among Pythonistas to create special [`__repr__`](https://docs.python.org/3/reference/datamodel.html#object.__repr__) methods that return text closely resembling the code used to construct the object. `__repr__` of `1` returns `"1"`, and `__repr__` of `None` returns `"None"`. With this library, you can easily implement `__repr__` for your own classes following this convention.


## Table of contents

- [**Installation**](#installation)
- [**Basic usage**](#basic-usage)
- [**Filtering**](#filtering)
- [**Custom display of objects**](#custom-display-of-objects)
- [**Placeholders**](#placeholders)


## Installation

You can install [`printo`](https://pypi.org/project/printo) with `pip`:

```bash
pip install printo
```

You can also use [`instld`](https://github.com/pomponchik/instld) to quickly try this package and others without installing them.


## Basic usage

The main function in this library is `describe_data_object`; it returns a string representing what your object's initialization code should look like. There are three required positional parameters:

- The name of the class for which we are creating a representation.
- A `list` or `tuple` of positional arguments.
- A `dict` with keyword arguments, where the keys are the names of the arguments, and the values are any objects.

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

You can prevent individual parameters from being displayed. To do this, pass a `dict` to the `filters` parameter. Keys identify arguments by index or name. Values are functions returning `bool`, where `True` keeps the argument and `False` skips it:

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

You can also use the built-in `not_none` filter to automatically exclude `None` values:

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

By default, all argument values are represented in the same way as the standard [`repr`](https://docs.python.org/3/library/functions.html#repr) function. There are only three exceptions:

- For regular functions, the function name is displayed.
- For classes, the class name is displayed.
- For lambda functions, just the `λ` symbol is displayed. This is done because there is no reliable way to display the source code of a lambda function in Python.

You can provide a custom `repr` function for all your objects; use the `serializer` parameter for this:

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

For individual parameters, you can pass predefined strings that will be displayed instead of the actual values. This can be useful, for example, to hide the values of secret fields when serializing objects.

Use the `placeholders` parameter for this by passing a dictionary, where the keys are argument names (for keyword arguments) or indices (for positional parameters, zero-indexed), and the values are strings:

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
