# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.7.6.dev0'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='genweb.serveistic',
      version=version,
      description="Funcionalitats dels serveis tic UPC",
      long_description=README + "\n" + HISTORY,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='tic',
      author='Plone Team',
      author_email='ploneteam@upcnet.es',
      url='https://github.com/UPCnet/genweb.serveistic',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['genweb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.dexteritytextindexer',
          'eea.facetednavigation',
          'simplejson',
          'google-api-python-client',
          'oauth2client',
          'pyOpenSSL',
      ],
      extras_require={'test': ['mock',
                               'plone.app.testing',
                               'plone.app.testing[robot]>=4.2.2',
                               'plone.app.robotframework[debug]']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
