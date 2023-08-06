"""
Flask-Session-Imp

-------------

Flask-Session is an extension for Flask that adds support for 
Server-side Session to your application.

just modify on 'flask_session'

`````
* `development version
  <https://github.com/mikezone/flask-session/master#egg=Flask-dev>`_

"""
from setuptools import setup


setup(
    name='Flask-Session-Imp',
    version='0.0.1',
    url='https://github.com/mikezone/flask-session',
    license='BSD',
    author='mike_chang',
    author_email='82643885@qq.com',
    description='Adds server-side session support to your Flask application',
    long_description=__doc__,
    packages=['flask_session_imp'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8'
    ],
    test_suite='test_session',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
