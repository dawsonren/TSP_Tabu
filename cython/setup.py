from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        ["cython/search_cy.pyx", "cython/tsp_cy.pyx"], 
        compiler_directives={"language_level": "3"}
    ),
    package_dir={'': 'cython'}
)