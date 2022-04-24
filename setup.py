import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='rackfocus',
    version='1.2.0',
    author='Antriksh Yadav',
    author_email='antrikshy@gmail.com',
    description=('CLI utility to download and compile '
                 'IMDb datasets into an SQLite database.'),
    long_description=long_description,
    url='https://github.com/Antrikshy/Rackfocus',
    packages=['rackfocus'],
    entry_points = {
        'console_scripts': [
            'rackfocus=rackfocus.run:main'
        ]
    },
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Database'
    ],
)
