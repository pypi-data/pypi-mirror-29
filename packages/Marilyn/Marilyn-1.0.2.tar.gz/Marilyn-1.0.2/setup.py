import os
import re

from distutils.core import setup


def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fp:
        return fp.read()


def _get_version_match(content, value_name):
    regex = r"^{} = ['\"]([^'\"]*)['\"]".format(value_name)
    version_match = re.search(regex, content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def get_value(value_name):
    path = os.path.join('Marilyn', '__init__.py')

    return _get_version_match(read_file(path), value_name)


setup(
    name='Marilyn',
    packages=['Marilyn'],  # this must be the same as the name above
    version=get_value('__version__'),
    description='Marilyn SDK',
    author=get_value('__author__'),
    author_email=get_value('__email__'),
    url='https://github.com/skar404/marilyn/',  # use the URL to the github repo
    download_url='https://github.com/skar404/marilyn/archive/master.zip',  # I'll explain this in a second
    keywords=['marilyn', 'sdk', 'api'],  # arbitrary keywords

    install_requires=['requests'],

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
