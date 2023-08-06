from distutils.core import setup


setup( name = "faketree",
       url = "https://bitbucket.org/mjr129/faketree",
       version = "0.0.0.28",
       description = "Fakes a genetic tree.",
       author = "Martin Rusilowicz",
       license = "https://www.gnu.org/licenses/agpl-3.0.html",
       packages = ["faketree"],
       entry_points = { "console_scripts": ["faketree = faketree.__main__:main"] },
       install_requires = ["intermake",
                           "mhelper",
                           "mgraph",
                           "stringcoercion"],
       python_requires = ">=3.6"
       )
