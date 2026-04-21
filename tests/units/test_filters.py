from printo import not_none


def test_not_none():
    assert not_none(None) == False

    assert not_none(1) == True
    assert not_none('lol') == True
    assert not_none('None') == True
    assert not_none(False) == True
    assert not_none(0) == True
    assert not_none('') == True
