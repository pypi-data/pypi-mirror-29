from distutils.core import setup


setup( name = "mgraph",
       url = "https://bitbucket.org/mjr129/mgraph",
       version = "1.0.0.2",
       description = "Yet another graphing library. This library supports Groot, providing functionality for dealing with graphs somewhere on the phylogenetic tree/network border.",
       author = "Martin Rusilowicz",
       license = "https://www.gnu.org/licenses/agpl-3.0.html",
       packages = ["mgraph"],
       python_requires = ">=3.6",
       install_requires = ["ete3",
                           "mhelper"]
       )
