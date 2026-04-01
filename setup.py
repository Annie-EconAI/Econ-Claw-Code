from setuptools import find_packages, setup

setup(
    name='econ-claw-code',
    version='0.1.0',
    description='CLI tool for economics and social science empirical research — from research question to submission',
    packages=find_packages(),
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'econ-claw=src.main:main',
        ],
    },
)
