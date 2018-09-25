import os
from codecs import open
from setuptools import setup


here_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here_dir, '__about__.py')) as f:
    exec(f.read(), about)


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    py_modules=['async_vk_api'],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    install_requires=['asks', 'trio']
)
