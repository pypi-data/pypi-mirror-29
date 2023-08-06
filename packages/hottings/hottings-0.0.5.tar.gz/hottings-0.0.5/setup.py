from setuptools import setup, find_packages

setup(
    name='hottings',
    version='0.0.5',
    description='A command line tool to manage hot reload tasks',
    author='jeremaihloo',
    author_email='jeremaihloo1024@gmail.com',
    url='https://github.com/jeremaihloo/hottings',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'hottings=hottings:main',
        ],
    },
    install_requires=[
        'watchdog',
        'jsonpickle',
        'click'
    ],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/jeremaihloo/hottings/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/jeremaihloo/hottings',
    },
)
