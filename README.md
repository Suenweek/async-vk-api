[![Build Status](https://travis-ci.com/Suenweek/async-vk-api.svg?branch=master)](https://travis-ci.com/Suenweek/async-vk-api)
[![codecov](https://codecov.io/gh/Suenweek/async-vk-api/branch/master/graph/badge.svg)](https://codecov.io/gh/Suenweek/async-vk-api)

# async-vk-api

Async VK API built with [asks](https://github.com/theelous3/asks)
and [trio](https://github.com/python-trio/trio).

Inspired by [vk](https://github.com/voronind/vk).

## Installation

#### Stable from PyPi
```bash
pip install async-vk-api
```

#### Latest from Github
```bash
pip install git+https://github.com/Suenweek/async-vk-api#egg=async-vk-api
```

## Usage

```python
import os

import trio
import async_vk_api


async def main():
    access_token = os.getenv('VK_API_ACCESS_TOKEN')
    api = async_vk_api.make_api(access_token, version='5.89')
    users = await api.users.get(user_ids=1)
    print(users)


if __name__ == '__main__':
    trio.run(main)
```

For the list of available methods see https://vk.com/dev/methods.
