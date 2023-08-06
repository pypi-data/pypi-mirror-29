from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()
with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='certbot-redis',  # Required
    version='0.1.0',  # Required
    description='Certbot plugin for Redis',
    url='https://github.com/deathowl/certbot-redis',  # Optional

    author='Balint Csergo',  # Optional

    author_email='<bcsergo@emarsys.com>',  # Optional

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='certbot redis',  # Optional

    packages=find_packages(),  # Required

    install_requires=install_requires,
    entry_points={
        'letsencrypt.plugins': [
            'redis = certbot_redis.plugin:Authenticator',
        ],
    },



)