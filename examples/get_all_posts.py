import os
import itertools

import trio
import async_vk_api


async def get_all_posts(owner_id):
    api = async_vk_api.make_api(
        access_token=os.getenv('VK_API_ACCESS_TOKEN'),
        version='5.92'
    )
    max_count = 100

    for offset in itertools.count(step=max_count):
        response = await api.wall.get(
            owner_id=owner_id,
            offset=offset,
            count=max_count
        )
        posts = response['items']
        if not posts:
            return
        for post in posts:
            yield post


async def main():
    async for post in get_all_posts(owner_id=1):
        print(post)


if __name__ == '__main__':
    trio.run(main)
