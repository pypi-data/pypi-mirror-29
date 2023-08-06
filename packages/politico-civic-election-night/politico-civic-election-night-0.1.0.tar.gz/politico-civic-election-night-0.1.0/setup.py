from setuptools import find_packages, setup

setup(
    name='politico-civic-election-night',
    version='0.1.0',
    description='',
    url='https://github.com/The-Politico/politico-civic-election-night',
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
        'celery',
        'django-cors-headers',
        'django',
        'djangorestframework',
        'dj-database-url',
        'elex',
        'politico-civic-entity',
        'politico-civic-geography',
        'politico-civic-government',
        'politico-civic-election',
        'politico-civic-demography',
        'politico-civic-vote',
        'politico-civic-almanac',
        'psycopg2',
    ],

    extras_require={
        'test': ['pytest'],
    },
)
