from setuptools import setup, find_packages
import os
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()

setup(
    name='seaborn-request-client',
	version='0.0.3',
    description='Request Client creates and maintains connections using '
                'the request library, but make each url endpoint a remote'
                'procedure call with the response content returned.  '
                'These function calls can made from a "connection" which has'
                'a hierarchy of objects that mirrors the hierarchy of the '
                'API.',
    long_description=long_description,
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/RequestClient',
    packages=['seaborn'] + ['seaborn.' + i
                            for i in find_packages(where='./seaborn')],
    install_requires=[
        'seaborn-meta',
        'pyopenssl',
        'gevent',
        'requests',
    ],
    extras_require={'test': ['test-chain',
                             'seaborn-flask'],
                    },
    license='MIT License',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    )
)
