from setuptools import setup, find_packages


setup(
    name='async-vk-api',
    version='0.6.0',
    description='Async VK API built with asks and trio',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Suenweek/async-vk-api',
    author='Roman Novatorov',
    author_email='roman.novatorov@gmail.com',
    install_requires=['asks', 'trio']
)
