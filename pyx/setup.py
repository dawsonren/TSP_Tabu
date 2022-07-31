from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        ["pyx/search_cy.pyx", "pyx/tsp_cy.pyx"], 
        compiler_directives={"language_level": "3"}
    ),
    package_dir={'': 'pyx'}
)