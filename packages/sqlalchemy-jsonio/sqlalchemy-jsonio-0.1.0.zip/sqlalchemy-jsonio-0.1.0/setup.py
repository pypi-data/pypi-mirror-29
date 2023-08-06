from setuptools import setup, find_packages

setup(
    name='sqlalchemy-jsonio',
    version='0.1.0',
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/RiceKab/sqlalchemy-jsonio',
    license='MIT',
    author='Kevin CY Tang',
    author_email='kevin@cyborn.be',
    keywords='sqlalchemy json jsonschema',
    description="Tool for conversion between SQLAlchemy entities and JSON format dictionaries. Includes validation using jsonschema."
                "Also contains CLI to generate schemas.",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['click', 'SQLAlchemy', 'jsonschema'],
    test_requires=["pytest"],
    python_requires='>=2.7',
    entry_points='''
        [console_scripts]
        jsonio=sqlalchemy_jsonio.cli:cli_main
    '''
)
