#!/usr/bin/env python

from setuptools import setup

setup(
    name='bayesloop',
    packages=['bayesloop'],
    version='1.4',
    description='Probabilistic programming framework that facilitates objective model selection for time-varying parameter models.',
    url='http://bayesloop.com',
    download_url = 'https://github.com/christophmark/bayesloop/tarball/1.4',
    author='Christoph Mark',
    author_email='christoph.mark@fau.de',
    license='The MIT License (MIT)',
    install_requires=['numpy>=1.11.0', 'scipy>=0.17.1', 'sympy>=1.0', 'matplotlib>=1.5.1', 'tqdm>=4.10.0', 'dill>=0.2.5'],
    keywords = ['bayes', 'inference', 'fitting', 'model selection', 'hypothesis testing', 'time series', 'time-varying', 'marginal likelihood'],
    classifiers = [],
    )
