from setuptools import setup

setup(
    name='django-embedly',
    version='0.1',
    description='Provides a template filter to parse embed URLs and talk to embedly API',
    author='Bay Citizen',
    author_email='info@baycitizen.org',
    url='http://github.com/BayCitizen/django-embedly/',
    packages=[
        'embeds',
    ],

    install_requires=[
        'distribute',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
