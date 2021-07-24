# -*- coding: utf-8 -*-
from setuptools import setup

long_description = u"""
Dispersive XES
==============

A pipeline for the ParSeq framework that implements data processing of XES
spectra measured in energy dispersive geometry. The energy dispersive image is
projected onto the base set of images given by the scanned elastically
scattered band.

This pipeline also serves as an example for creating analysis nodes, transforms
that connect these nodes and widgets that set options and parameters of the
transforms.

Dependencies
------------

parseq -- the framework package.
silx -- is used for plotting and Qt imports.

How to use
----------

Either install ParSeq and this pipeline application by their installers or put
their folders near by (i.e. in the same folder), rename them as `parseq` and
`parseq_XES_dispersive` and run `python XES_dispersive_start.py`. You can try
it with `--test` to load test data and/or `--noGUI` but an assumed pattern is
to load a project file; use the test project file located in
`parseq_XES_dispersive/saved`.

"""

setup(
    name='parseq_XES_dispersive',
    version='0.1.0',
    description='A pipeline for data processing of energy dispersive XES',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Konstantin Klementiev',
    author_email='konstantin.klementiev@gmail.com',
    project_urls={'Source': 'https://github.com/kklmn/ParSeq-XES-dispersive'},
    platforms='OS Independent',
    license='MIT License',
    keywords='data-analysis pipeline framework gui synchrotron spectroscopy',
    # python_requires=,
    zip_safe=False,  # True: build zipped egg, False: unzipped
    packages=['parseq_XES_dispersive'],
    package_dir={'parseq_XES_dispersive': '.'},
    package_data={
        'parseq_XES_dispersive': ['*.py', '*.md', 'LICENSE',
                                  'data/*.*', 'doc/_images/*.*', 'saved/*.*']},
    scripts=['XES_dispersive_start.py'],
    install_requires=['numpy>=1.8.0', 'scipy>=0.17.0', 'matplotlib>=2.0.0',
                      'sphinx>=1.6.2', 'h5py', 'silx'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Science/Research',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Intended Audience :: Science/Research',
                 'Topic :: Graphical User Interface']
    )
