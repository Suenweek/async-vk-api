import pytest

from async_vk_api import retry


async def test_single_exception():
    exc = RuntimeError
    attempts = 4
    n = 0

    @retry.on(exc, attempts=attempts)
    async def func():
        nonlocal n
        n += 1
        raise exc

    with pytest.raises(exc):
        await func()

    assert n == attempts


async def test_multiple_exceptions():
    exc1, exc2 = ValueError, TypeError
    attempts = 2
    n = 0

    @retry.on((exc1, exc2), attempts=attempts)
    async def func():
        nonlocal n
        n += 1

        if n == 1:
            raise exc1
        elif n == 2:
            raise exc2
        else:
            assert not 'Reachable'

    with pytest.raises(exc2):
        await func()

    assert attempts == n
