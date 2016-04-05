from distutils.core import setup
from Cython.Build import cythonize
import sys
sys.argv += ['build_ext', '--inplace']

setup(
    ext_modules = cythonize("bmpFlowModFast.pyx")
)


