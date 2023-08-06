#!/usr/bin/env python
from distutils.core import setup, Extension

sources = [
    "crypto/aesb.c",
    "crypto/oaes_lib.c",
    "crypto/c_keccak.c",
    "crypto/c_groestl.c",
    "crypto/c_blake256.c",
    "crypto/c_jh.c",
    "crypto/c_skein.c",
    "crypto/hash.c",

    "cryptonite_hash.c",
    "cryptolite_hash.c",
    "sysinfos.c",
    "cryptonitehashmodule.c",
]

depends = [
    "compat.h",
    "miner.h",
    "cryptonite_hash.h",

    "compat/cpuminer-config.h",
    "compat/inttypes.h",
    "compat/stdbool.h",
    "compat/unistd.h",
    "compat/winansi.h",
]

include_dirs = [
    'include/pybind11',
    'compat',
    'crypto',
    '.',
]

library_dirs = [
    'compat',
    'crypto',
    '.'
]

define_macros = [('NOASM', '1'), ]

pycryptonight = Extension('pycryptonight',
                          sources=sources,
                          depends=depends,
                          extra_compile_args=["-I .", "-std=gnu99", "-Wall"],
                          include_dirs=include_dirs,
                          library_dirs=library_dirs,
                          define_macros=define_macros,
                          )


setup(
    name='pycryptonight',
    author="Written by Sumokoin, and Packaged by Command",
    author_email="maoxs2@gmail.com",
    license='GPL',
    version='0.0.1',
    url='https://github.com/maoxs2/pycryptonight',
    description=('Python wrappers for CryptoNight'),
    ext_modules=[pycryptonight],
)
