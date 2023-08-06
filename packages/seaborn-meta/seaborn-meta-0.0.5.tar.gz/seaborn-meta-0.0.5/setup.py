from setuptools import setup, find_packages
import os
try:
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        long_description = f.read()
except:
    long_description = ''

setup(
    name='seaborn-meta',
	version='0.0.5',
    description='SeabornMeta allows for simple changing'
                'of names between conventions, as well'
                'as auto-generating init files',
    long_description=long_description,
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/meta',
    download_url='https://github.com/SeabornGames/meta'
                 '/tarball/download',
    keywords=['meta'],
    install_requires=[
        'seaborn-hack',
    ],
    extras_require={
    },
    packages=['seaborn'] + ['seaborn.' + i
                            for i in find_packages(where='./seaborn')],
    license='MIT License',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
)
