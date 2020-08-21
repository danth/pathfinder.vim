from pathfinder.debytes import debytes


def test_debytes_bytes():
    assert debytes(b"hello world") == "hello world"


def test_debytes_str():
    assert debytes("hello world") == "hello world"
