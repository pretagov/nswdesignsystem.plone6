# -*- coding: utf-8 -*-
"""Installer for the nswdesignsystem.plone6 package."""

from setuptools import find_packages, setup

long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="nswdesignsystem.plone6",
    version="0.3.0",
    description="Plone backend package for the NSW Design system",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="PretaGov",
    author_email="jeff.bledsoe@pretagov.com.au",
    url="https://github.com/collective/nswdesignsystem.plone6",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/nswdesignsystem.plone6",
        "Source": "https://github.com/collective/nswdesignsystem.plone6",
        "Tracker": "https://github.com/collective/nswdesignsystem.plone6/issues",
        # 'Documentation': 'https://nswdesignsystem.plone6.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["nswdesignsystem"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "plone.api>=1.8.4",
        "plone.app.dexterity",
        "collective.volto.formsupport==2.6.2",
        "collective.volto.formsupport[recaptcha]",
        "collective.volto.formsupport[honeypot]",
        "collective.volto.subfooter==1.1.0",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = nswdesignsystem.plone6.locales.update:update_locale
    """,
)
