import pytest

from async_vk_api import ApiError


async def test_api(api):
    # Response OK
    response = await api.users.get(
        user_ids='1,2,3',
        fields='city,verified'
    )
    assert response['method_name'] == 'users.get'
    assert response['params']['user_ids'] == '1,2,3'
    assert response['params']['fields'] == 'city,verified'
    assert 'v' in response['params']

    # Response error
    try:
        await api.users.get(
            user_ids='1,2,3',
            fields='city,verified',
            _key='error'
        )
    except ApiError as exc:
        response = exc.args[0]
        assert response['method_name'] == 'users.get'
        assert response['params']['user_ids'] == '1,2,3'
        assert response['params']['fields'] == 'city,verified'
        assert 'v' in response['params']
    else:
        pytest.fail()
