from setuptools import setup


setup(
    name='async-vk-api',
    version='0.0.8',
    description='Python async VK API',
    py_modules=['async_vk_api'],
    url='https://github.com/Suenweek/async-vk-api',
    author='Roman Novatorov',
    author_email='roman.novatorov@gmail.com',
    install_requires=['asks', 'trio']
)
