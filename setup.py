import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-jasperreports',
    version='v1.0.3.alpha1',
    packages=find_packages(),
    package_data = {
        '': ['*.xml', '*.jrxml', '*.jar', '*.py', '*.sh'],
    },
    include_package_data=True,
    license='BSD License',  # example license
    description='Django app to export jasperreports to pdf.',
    long_description=README,
    #url='https://www.example.com/',
    author='Gloria Martinez Hidalgo',
    author_email='gloriamh@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
