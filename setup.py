from setuptools import setup, find_packages
from track.core.version import get_version

VERSION = get_version()

f = open("README.md", "r")
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name="track",
    version=VERSION,
    description="Tracks time.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Jakub Nowicki",
    author_email="q.nowicki@gmail.com",
    url="https://github.com/jakubnowicki/track",
    license="LGPL-3",
    packages=find_packages(exclude=["ez_setup", "tests*"]),
    package_data={"track": ["templates/*"]},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        track = track.main:main
    """,
)
