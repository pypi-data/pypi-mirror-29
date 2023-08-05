from setuptools import setup

lib_name = 'silph.models'

setup(
    name=lib_name,
    version='0.4.5',
    author='Marco Ceppi',
    author_email='marco@thesilphroad.com',
    description='Database models for TSR',
    license='other',
    classifiers=[
        'License :: Other/Proprietary License',
        'Topic :: Database',
        'Development Status :: 5 - Production/Stable',
    ],
    namespace_packages=['silph'],
    packages=[lib_name],
    install_requires=[
        'asyncqlio==0.1.1.dev117',
        'aiomysql',
    ],
    dependency_links=[
        'git+https://github.com/Unplottable/asyncqlio.git@discord-bot#egg=asyncqlio-0.1.1.dev117',
    ]
)
