from __future__ import unicode_literals

import os
import sys
import pypandoc

from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (OSError, IOError, ImportError):
    long_description = open('README.md').read()


def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner = ['pytest-runner>=2.9'] if needs_pytest else []

    setup_requires = [] + pytest_runner
    install_requires = ['numpy', 'scipy', 'limix-core']
    tests_require = ['pytest']

    console_scripts = [
        'struct_lmm_analyze=struct_lmm.scripts.struct_lmm_analyze:entry_point',
        'lmm_analyze=struct_lmm.scripts.lmm_analyze:entry_point',
        'lmm_int_analyze=struct_lmm.scripts.lmm_int_analyze:entry_point',
        'norm_env=struct_lmm.scripts.norm_env:entry_point'
    ]

    readme = open('README.md').read()
    long_description = pypandoc.convert_text(
            readme, 'rst', format='markdown')
 

    metadata = dict(
        name='struct-lmm',
        version='0.0.2',
        maintainer="StructLMM developers",
        maintainer_email="casale@ebi.ac.uk",
        license="Apache License 2.0'",
        #description="Linear mixed model",
        long_description=long_description,
        url='https://github.com/limix/struct-lmm',
        packages=find_packages(),
        zip_safe=False,
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_require=tests_require,
        include_package_data=True,
        entry_points={'console_scripts': console_scripts})

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)


if __name__ == '__main__':
    setup_package()
