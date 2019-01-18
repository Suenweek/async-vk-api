import trio
import pytest

from async_vk_api.throttler import Throttler


@pytest.mark.parametrize(['n_workers', 'rate', 'job_duration'], [
    # Fast workers
    (4, 2, 1),

    # Slow workers
    (4, 2, 3)
])
async def test_throttler(n_workers, rate, job_duration, autojump_clock):
    calls = []

    throttler = Throttler(rate)
    assert not throttler.locked

    async def worker():
        async with throttler():
            assert throttler.locked
            await trio.sleep(job_duration)
            calls.append(trio.current_time())

    async with trio.open_nursery() as nursery:
        for _ in range(n_workers):
            nursery.start_soon(worker)

    assert n_workers == len(calls)

    for a, b in zip(calls, calls[1:]):
        assert pytest.approx(rate, b - a)
