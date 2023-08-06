from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

version = '0.2.2'

setup(
    name='djob',
    version=version,
    description="djob",
    long_description=README,
    classifiers=[],
    keywords='djob',
    author='me',
    author_email='me@example.org',
    url='https://example.org',
    license='LGPL v3',
    zip_safe=True,
    py_modules=['djob'],
    include_package_data=True,
    package_dir={},
    install_requires=[
        'click',
        'prettytable',
        'configobj',
    ],
    entry_points='''
        [console_scripts]
        djob=djob:main
    ''',
)
