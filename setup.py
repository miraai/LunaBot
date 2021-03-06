from setuptools import setup

setup(
    name='lunabot',
    version='0.0.1',
    packages=['cogs'],
    install_requires=[
        'discord.py',
        'discord.py[voice]',
        'asyncio',
        'aiohttp',
        'websockets',
        'lxml',
        'pytest'
    ],
    tests_require=["pytest"],
    zip_safe=False,
)