from setuptools import find_packages, setup

setup(
    name='politico-civic-government',
    version='0.1.0',
    description='',
    url='https://github.com/The-Politico/politico-civic-government',
    author='POLITICO interactive news',
    author_email='interactives@politico.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='',

    packages=find_packages(exclude=['docs', 'tests', 'example']),

    install_requires=[
        'django',
        'djangorestframework',
        'dj-database-url',
        'psycopg2',
        'politico-civic-entity',
        'politico-civic-geography',
        'tqdm',
        'us',
    ],

    extras_require={
        'test': ['pytest'],
    },
)
