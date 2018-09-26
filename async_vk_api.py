import os
import trio
import asks


asks.init(trio)


class ApiError(Exception):
    pass


class Api:

    def __init__(
        self,
        access_token=os.getenv('VK_ACCESS_TOKEN'),
        version='5.85',
        base_url='https://api.vk.com',
        base_endpoint='/method',
        connections=1,
        requests_per_second=3,
    ):
        self.access_token = access_token
        self.version = version
        self.session = asks.Session(
            base_location=base_url,
            endpoint=base_endpoint,
            connections=connections
        )
        self._rate = 1 / requests_per_second
        self._lock = trio.Lock()

    async def __call__(self, method_name, **params):
        response = None

        async def func():
            nonlocal response
            response = await self._call(method_name, **params)

        tick_finished = trio.Event()

        async def tick():
            await trio.sleep(self._rate)
            tick_finished.set()

        await self._lock.acquire()

        async with trio.open_nursery() as nursery:
            nursery.start_soon(func)
            nursery.start_soon(tick)

            await tick_finished.wait()
            self._lock.release()

        return response

    async def _call(self, method_name, **params):
        params.update(
            access_token=self.access_token,
            v=self.version
        )
        response = await self.session.get(
            path=f'/{method_name}',
            params=params
        )
        payload = response.json()

        try:
            return payload['response']
        except KeyError:
            raise ApiError(payload['error'])

    def __getattr__(self, item):
        return _MethodGroup(name=item, api=self)


class _MethodGroup:

    def __init__(self, name, api):
        self.name = name
        self.api = api

    def __getattr__(self, item):
        return _Method(name=item, group=self)


class _Method:

    def __init__(self, name, group):
        self.name = name
        self.group = group

    @property
    def full_name(self):
        return f'{self.group.name}.{self.name}'

    async def __call__(self, **params):
        return await self.group.api(self.full_name, **params)
