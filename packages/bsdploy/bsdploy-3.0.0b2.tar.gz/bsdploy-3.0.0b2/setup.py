from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

version = "3.0.0b2"

install_requires = [
    'PyYAML',
    'jinja2',
    'setuptools',
    'ploy>=2dev',
    'ploy_ansible>=2.0.0b2',
    'ploy_ezjail>=2dev',
    'ploy_fabric>=2dev',
]

setup(
    name="bsdploy",
    version=version,
    description="A tool to remotely provision, configure and maintain FreeBSD jails",
    long_description=README + '\n\n\nChanges\n=======\n\n' + CHANGES,
    author='Tom Lazar',
    author_email='tom@tomster.org',
    url='http://github.com/ployground/bsdploy',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
    ],
    license="BSD 3-Clause License",
    zip_safe=False,
    packages=['bsdploy'],
    install_requires=install_requires,
    extras_require={
        'development': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'coverage',
            'jarn.mkrelease',
            'ploy_virtualbox>=2dev',
            'pytest >= 2.4.2',
            'pytest-flakes',
            'pytest-pep8',
            'tox',
            'mock',
        ],
    },
    entry_points="""
        [console_scripts]
        ploy-download = bsdploy.download:run
        [ansible_paths]
        bsdploy = bsdploy:ansible_paths
        [ploy.plugins]
        bsdploy = bsdploy:plugin
    """)
