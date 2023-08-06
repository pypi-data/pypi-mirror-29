import setuptools


setuptools.setup(
    name='consumers',
    version='0.6.0',
    description='A simple, flexible way to parallelize processing in Python.',
    long_description=open('README.rst').read(),
    author='Andrew Rabert',
    author_email='arabert@nullsum.net',
    url='https://github.com/nvllsvm/consumers',
    license='Apache 2.0',
    packages=['consumers'],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only'
    ),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    zip_safe=True
)
