from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print('warning: pypandoc module not found, could not convert Markdown to RST')
    read_md = lambda f: open(f, 'r').read()

setup(name='csvtsdb',
    version='0.1.3',
    description='CSV-backed timeseries database usable standalone or as a Twisted resource',
    long_description=read_md('README.md'),
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
