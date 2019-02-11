import pytest

from async_vk_api.namespace import Namespace


def test_create_from_dict():
    d = {'foo': 'bar', 'spam': 42}
    ns = Namespace.from_dict(d)
    assert ns.__dict__ == d


def test_comparison():
    ns1 = Namespace(one=1, two=2)
    ns2 = Namespace(two=2, three=3)
    assert ns1 != ns2

    ns1.three = 3
    ns2.one = 1
    assert ns1 == ns2

    assert ns1 != {'one': 1, 'two': 2, 'three': 3}


def test_iteration():
    ns = Namespace()
    assert list(ns) == []
    assert dict(ns) == {}

    ns.foo = 'bar'
    ns.spam = 42
    assert list(ns) == [('foo', 'bar'), ('spam', 42)]
    assert dict(ns) == {'foo': 'bar', 'spam': 42}


def test_repr():
    d = {'foo': 'bar', 'spam': 42}
    ns = Namespace(**d)
    assert repr(ns) == repr(d)


def test_access():
    ns = Namespace()

    with pytest.raises(AttributeError):
        ns.foo
        pytest.fail('Unreachable')

    with pytest.raises(KeyError):
        ns['foo']
        pytest.fail('Unreachable')

    ns.foo = 'bar'
    assert ns['foo'] == ns.foo


@pytest.mark.parametrize('name', ['def', ' '])
def test_invalid_attr_name(name):
    with pytest.raises(ValueError):
        Namespace.from_dict({name: name})
