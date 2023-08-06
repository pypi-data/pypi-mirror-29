from distutils.core import setup

from Marilyn import __version__, __author__, __email__

setup(
    name='Marilyn',
    packages=['Marilyn'],  # this must be the same as the name above
    version=__version__,
    description='Marilyn SDK',
    author=__author__,
    author_email=__email__,
    url='https://github.com/skar404/marilyn/',  # use the URL to the github repo
    download_url='https://github.com/skar404/marilyn/archive/master.zip',  # I'll explain this in a second
    keywords=['marilyn', 'sdk', 'api'],  # arbitrary keywords
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
