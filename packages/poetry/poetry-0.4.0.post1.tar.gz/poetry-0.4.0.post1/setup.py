from distutils.core import setup

packages = \
['poetry',
 'poetry.console',
 'poetry.console.commands',
 'poetry.console.styles',
 'poetry.installation',
 'poetry.io',
 'poetry.layouts',
 'poetry.masonry',
 'poetry.masonry.builders',
 'poetry.masonry.publishing',
 'poetry.masonry.utils',
 'poetry.mixology',
 'poetry.mixology.contracts',
 'poetry.mixology.graph',
 'poetry.packages',
 'poetry.puzzle',
 'poetry.puzzle.operations',
 'poetry.repositories',
 'poetry.semver',
 'poetry.semver.constraints',
 'poetry.toml',
 'poetry.toml.prettify',
 'poetry.toml.prettify.elements',
 'poetry.toml.prettify.elements.traversal',
 'poetry.toml.prettify.lexer',
 'poetry.toml.prettify.parser',
 'poetry.toml.prettify.tokens',
 'poetry.utils',
 'poetry.vcs',
 'poetry.version']

package_data = \
{'': ['*']}

install_requires = \
['cleo (>=0.6.0.0,<0.7.0.0)',
 'requests (>=2.18.0.0,<3.0.0.0)',
 'toml (>=0.9.0.0,<0.10.0.0)',
 'cachy (>=0.1.0.0,<0.2.0.0)',
 'pip-tools (>=1.11.0.0,<2.0.0.0)',
 'requests-toolbelt (>=0.8.0.0,<0.9.0.0)']

entry_points = \
{'console_scripts': ['poetry = poetry:console.run']}

setup(
    name='poetry',
    version='0.4.0.post1',
    description='Python dependency management and packaging made easy.',
    author='Sébastien Eustace',
    author_email='sebastien@eustace.io',
    url='https://poetry.eustace.io/',
    packages=packages,
    package_data=package_data,
    install_requires=install_requires,
    entry_points=entry_points,
    python_requires='>=3.6.0.0,<4.0.0.0',
)
