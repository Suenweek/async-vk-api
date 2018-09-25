import sys
import asks
asks.init('trio')


class ApiError(Exception):
    pass


class Api:

    DEFAULT_VERSION = '5.85'
    BASE_URL = 'https://api.vk.com'
    BASE_ENDPOINT = '/method'

    def __init__(
        self,
        access_token,
        version=DEFAULT_VERSION,
        base_url=BASE_URL,
        base_endpoint=BASE_ENDPOINT
    ):
        self.access_token = access_token
        self.version = version
        self.session = asks.Session(
            base_location=base_url,
            endpoint=base_endpoint
        )

    async def __call__(self, method_name, **params):
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
        return MethodGroup(name=item, api=self)


class MethodGroup:

    def __init__(self, name, api):
        self.name = name
        self.api = api

    def __getattr__(self, item):
        return Method(name=item, group=self)


class Method:

    def __init__(self, name, group):
        self.name = name
        self.group = group

    @property
    def full_name(self):
        return f'{self.group.name}.{self.name}'

    async def __call__(self, **params):
        return await self.group.api(self.full_name, **params)


sys.modules[__name__] = Api
