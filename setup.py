import os
from setuptools import setup

LONG_DESCRIPTION = """
The wq command line tool.
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    # Attempt to run pandoc on markdown file
    import subprocess
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open(os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        ))
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()


def create_wq_namespace():
    """
    Generate the wq namespace package
    (not checked in, as it technically is the parent of this folder)
    """
    if os.path.isdir("wq"):
        return
    os.makedirs("wq")
    init = open(os.path.join("wq", "__init__.py"), 'w')
    init.write("__import__('pkg_resources').declare_namespace(__name__)")
    init.close()


create_wq_namespace()

setup(
    name='wq.core',
    version='1.1.0',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='https://wq.io/',
    license='MIT',
    packages=['wq', 'wq.core'],
    package_dir={
        'wq.core': '.',
    },
    install_requires=[
        'click<6',
        'PyYAML',
    ],
    namespace_packages=['wq'],
    entry_points='''
       [console_scripts]
       wq=wq.core:wq
       [wq]
       wq.core=wq.core.info
    ''',
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Build Tools',
    ]
)
