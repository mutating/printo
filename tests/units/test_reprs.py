from printo.reprs import superrepr


def test_superrepr_basically_is_repr():
    assert superrepr(1) == "1"
    assert superrepr("hello") == "'hello'"
    assert superrepr([1, 2, 3]) == "[1, 2, 3]"
    assert superrepr({"a": 1, "b": 2}) == "{'a': 1, 'b': 2}"
    assert superrepr(None) == "None"
    assert superrepr(True) == "True"
    assert superrepr(False) == "False"
    assert superrepr(3.14) == "3.14"
    assert superrepr(1 + 2j) == "(1+2j)"
    assert superrepr([1, "hello", [2, 3]]) == "[1, 'hello', [2, 3]]"
    assert superrepr({"a": [1, 2], "b": {"c": 3}}) == "{'a': [1, 2], 'b': {'c': 3}}"


def test_superrepr_for_named_function():
    def function():
        pass

    assert superrepr(function) == "function"


def test_superrepr_for_lambda_function():
    assert superrepr(lambda x: x) == "lambda x: x"


def test_superrepr_for_lambda_functions_when_they_are_multple_in_one_line():
    lambdas = [lambda x: x, lambda y: y]

    assert superrepr(lambdas[0]) == "λ"
    assert superrepr(lambdas[1]) == "λ"
