from distutils.core import setup, Extension

spam_mod = Extension(
                'spam', 
                 sources = ['spammodule.c']
)
setup( name = "spam",
        version = "1.0",
        description = "A Sample extension module",
        ext_modules = [spam_mod],
)
