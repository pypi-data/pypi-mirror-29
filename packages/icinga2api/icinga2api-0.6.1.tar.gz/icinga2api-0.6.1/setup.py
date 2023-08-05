from setuptools import setup

PACKAGE = "icinga2api"
NAME = "icinga2api"
DESCRIPTION = "Python Icinga 2 API"
AUTHOR = "fmnisme, Tobias von der Krone"
AUTHOR_EMAIL = "fmnisme@gmail.com, tobias@vonderkrone.info"
URL = "https://github.com/tobiasvdk/icinga2api"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=["requests"],
    keywords="Icinga api",
    license="2-Clause BSD",
    url=URL,
    packages=[PACKAGE],
    zip_safe=False,
    long_description=open("README.txt").read(),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
