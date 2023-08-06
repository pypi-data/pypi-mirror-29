from setuptools import setup

setup(name='csvtsdb',
    version='0.1.2',
    description='CSV-backed timeseries database usable standalone or as a Twisted resource',
    long_description=open('README.md').read(),
    url='http://github.com/anotherkamila/csvtsdb',
    author='Kamila Součková',
    author_email='kamisouckova@gmail.com',
    license='MIT',
    packages=['csvtsdb'],
    install_requires=[
        'twisted',
        'klein',
    ]
)
