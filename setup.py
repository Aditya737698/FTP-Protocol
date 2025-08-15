from setuptools import setup, find_packages

setup(
    name='ftpserver',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ftpserver = ftpserver.core.server:main'
        ]
    }
)
