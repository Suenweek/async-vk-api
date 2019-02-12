from async_vk_api.factories import make_api


def test_make_api():
    api = make_api(
        access_token='test_access_token',
        version='test_version'
    )
    assert api._access_token == 'test_access_token'
    assert api._version == 'test_version'
    assert api._session.base_location == 'https://api.vk.com'
    assert api._session.endpoint == '/method'
