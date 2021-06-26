import setuptools

with open('README.md', 'r') as f:
    readme = f.read()

setuptools.setup(
    name='coll2merge',
    version='0.1.0',
    description='Merge *.coll2 files for Decked Builder',
    long_description=readme,
    author='Steven Dahdah',
    url='https://github.com/sdahdah/coll2merge',
    packages=setuptools.find_packages(exclude='tests'),
    entry_points={
        'console_scripts': ['coll2merge=coll2merge.coll2merge:main'],
    },
    install_requires=['pyaml'],
)
