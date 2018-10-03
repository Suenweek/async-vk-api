# async-vk-api

Async VK API built with [asks](https://github.com/theelous3/asks)
and [trio](https://github.com/python-trio/trio).

Inspired by [vk](https://github.com/voronind/vk).


## Installation

```bash
pip install git+https://github.com/Suenweek/async-vk-api#egg=async-vk-api
```


## Usage

```python
import trio
import async_vk_api as vk

api = vk.Api('YOUR_ACCESS_TOKEN')

async def main():
    users = await api.users.get(user_ids=1)
    print(users)

trio.run(main)
```

For the list of available methods see https://vk.com/dev/methods.
