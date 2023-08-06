"""
A python package for working with the Global Electronic Party Information Registry (GEPIR) SOAP API.
"""
from setuptools import setup, find_packages

setup(
    name='gepir',

    version='4.0.2',

    description="A python client package for querying GEPIR.",

    # The project's main homepage.
    url='https://bitbucket.com/davebelais/gepir',

    # Author details
    author='David Belais',
    author_email='david@belais.me',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='gepir gs1 gtin gln gcp',

    packages=find_packages(exclude=['docs', 'tests']),
    # packages=[], # explicitly set packages
    # py_modules=[], # Single-file module names

    # dependencies
    # See https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'future>=0.15.2'
    ],

    # pip install -e .[dev,test]
    extras_require={
        'dev': [
            'pytest>=2.9.0'
        ],
        'test': [
            'pytest>=2.9.0'
        ],
    },

    package_data={},

    # See http://docs.python.org/3.5/distutils/setupscript.html#installing-additional-files
    data_files=[],

    entry_points={
        'console_scripts': [],
    }
)
