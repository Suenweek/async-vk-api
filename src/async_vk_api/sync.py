import contextlib
import trio


class Throttler:

    def __init__(self, rate):
        self.rate = rate
        self._lock = trio.Semaphore(1)

    @contextlib.asynccontextmanager
    async def __call__(self):
        await self._lock.acquire()
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self._tick)
            yield

    async def _tick(self):
        await trio.sleep(self.rate)
        self._lock.release()
