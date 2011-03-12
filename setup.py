from setuptools import setup

setup(
    name='apropost',
    version='1.0',
    packages=['apropost'],
    include_package_data=True,

    requires=['Django', 'celery', 'redis',],
    install_requires=['Django', 'celery', 'redis',],
    # plus https://github.com/facebook/python-sdk.git
)
