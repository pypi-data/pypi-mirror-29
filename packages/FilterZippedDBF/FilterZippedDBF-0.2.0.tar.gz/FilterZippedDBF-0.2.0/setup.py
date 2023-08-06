# setup.py
# Copyright 2016 Roger Marsh
# Licence: See LICENSE.txt (BSD licence)

if __name__ == '__main__':

    from setuptools import setup, find_packages

    with open('README.rst') as file:
        long_description = file.read()

    setup(
        name='FilterZippedDBF',
        version='0.2.0',
        description=''.join(('Filter zipped DBF files to remove data ',
                             'from unwanted fields')),
        author='Roger Marsh',
        author_email='roger.marsh@solentware.co.uk',
        url='http://www.solentware.co.uk',
        packages=find_packages(),
        package_data={'filterzippeddbf':['help.*']},
        long_description=long_description,
        license='BSD',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        keywords='DBF CSV',
    )
