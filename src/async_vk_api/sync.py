import trio


class Throttle:

    def __init__(self, rate):
        self.rate = rate
        self.lock = trio.Lock()

    async def __call__(self, func, *args, **kwargs):
        rv = None

        async def call_func():
            nonlocal rv
            rv = await func(*args, **kwargs)

        ticked = trio.Event()

        async def tick():
            await trio.sleep(self.rate)
            ticked.set()

        await self.lock.acquire()

        async with trio.open_nursery() as nursery:
            nursery.start_soon(call_func)
            nursery.start_soon(tick)

            await ticked.wait()
            self.lock.release()

        return rv


def throttled(rate):

    throttle = Throttle(rate)

    def decorator(func):

        async def wrapper(*args, **kwargs):
            return await throttle(func, *args, **kwargs)

        return wrapper

    return decorator
