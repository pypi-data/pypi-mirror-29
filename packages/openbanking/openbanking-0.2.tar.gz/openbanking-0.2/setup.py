import os
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'openbanking', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(
  name = 'openbanking',
  packages = ['openbanking'], # this must be the same as the name above
  version=about['__version__'],
  description = 'Python 3 Client for UK Open Banking.',
  author = 'Glyn Jackson',
  author_email = 'me@glynjackson.org',
  url = 'https://bitbucket.org/glynjackson/openbanking',
  download_url = '',
  keywords = ['openbanking', 'open  banking', 'banking api'], # arbitrary keywords
  classifiers = [],
)



#
#
#

#
# with open('README', 'r',) as f:
#     readme = f.read()
# print(about['__title__'])
# setup(
#     name=about['__title__'],
#     packages=about['__title__'],

#     description=about['__description__'],
#     long_description=readme,
#     author=about['__author__'],
#     author_email=about['__author_email__'],
#     url=about['__url__'],
#     download_url='',
#     keywords=['openbanking', 'open  banking', 'banking api', "open banking uk"],
#     classifiers=[],
#     license=about['__license__'],
#     package_data={'': ['LICENSE', 'CONTRIBUTING.rst']},
#
# )
