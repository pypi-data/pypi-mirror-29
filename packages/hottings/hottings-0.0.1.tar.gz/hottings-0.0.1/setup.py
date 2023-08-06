from setuptools import setup, find_packages

setup(
    name='hottings',
    version='0.0.1',
    description='A command line tool to manage hot reload tasks',
    author='jeremaihloo',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'hottings=hottings.monitors:main',
        ],
    },
    package_data={  # Optional
        'sample': ['hottings.json'],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/jeremaihloo/hottings/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/jeremaihloo/hottings',
    },
)
