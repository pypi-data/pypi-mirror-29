Poetry: Dependency Management for Python
========================================

Poetry helps you declare, manage and install dependencies of Python
projects, ensuring you have the right stack everywhere.

.. figure:: https://raw.githubusercontent.com/sdispater/poetry/master/assets/install.gif
   :alt: Poet Install

   Poet Install

The package is **highly experimental** at the moment so expect things to
change and break. However, if you feel adventurous feedback and pull
requests are greatly appreciated.

Also, be aware that the features described here are the goal that this
library is aiming for and, as of now, not all of them are implemented.
The dependency management is pretty much done while the packaging and
publishin are not done yet.

And finally, Poetry's code is only compatible with Python 3.6+ but it
can manage Python project's with previous versions without any problem.

Installation
------------

.. code:: bash

    pip install poetry

Enable tab completion for Bash, Fish, or Zsh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``poetry`` supports generating completion scripts for Bash, Fish, and
Zsh. See ``poet help completions`` for full details, but the gist is as
simple as using one of the following:

.. code:: bash

    # Bash
    poetry completions bash > /etc/bash_completion.d/poetry.bash-completion

    # Bash (macOS/Homebrew)
    poetry completions bash > $(brew --prefix)/etc/bash_completion.d/poetry.bash-completion

    # Fish
    poetry completions fish > ~/.config/fish/completions/poetry.fish

    # Zsh
    poetry completions zsh > ~/.zfunc/_poetry

*Note:* you may need to restart your shell in order for the changes to
take effect.

For ``zsh``, you must then add the following line in your ``~/.zshrc``
before ``compinit``:

.. code:: zsh

    fpath+=~/.zfunc

Introduction
------------

``poetry`` is a tool to handle dependencies installation, building and
packaging of Python packages. It only needs one file to do all of that:
``poetry.toml``.

.. code:: toml

    [package]
    name = "pypoet"
    version = "0.1.0"
    description = "Poet helps you declare, manage and install dependencies of Python projects, ensuring you have the right stack everywhere."

    license = "MIT"

    authors = [
        "Sébastien Eustace <sebastien@eustace.io>"
    ]

    readme = 'README.md'

    repository = "https://github.com/sdispater/poet"
    homepage = "https://github.com/sdispater/poet"

    keywords = ['packaging', 'poet']

    include = ['poet/**/*', 'LICENSE']

    python-versions = "~2.7 || ^3.2"


    [dependencies]
    toml = "^0.9"
    requests = "^2.13"
    semantic_version = "^2.6"
    pygments = "^2.2"
    twine = "^1.8"
    wheel = "^0.29"
    pip-tools = "^1.8.2"
    cleo = { git = "https://github.com/sdispater/cleo.git", branch = "master" }

    [dev-dependencies]
    pytest = "^3.0"
    pytest-cov = "^2.4"
    coverage = "<4.0"
    httpretty = "^0.8.14"

    [scripts]
    poet = 'poet:app.run'

There are some things we can notice here:

-  It will try to enforce `semantic versioning <http://semver.org>`__ as
   the best practice in version naming.
-  You can specify the readme, included and excluded files: no more
   ``MANIFEST.in``. ``poetry`` will also use VCS ignore files (like
   ``.gitignore``) to populate the ``exclude`` section.
-  Keywords (up to 5) can be specified and will act as tags on the
   packaging site.
-  The dependencies sections support caret, tilde, wildcard, inequality
   and multiple requirements.
-  You must specify the python versions for which your package is
   compatible.

``poetry`` will also detect if you are inside a virtualenv and install
the packages accordingly. So, ``poetry`` can be installed globally and
used everywhere.

``poetry`` also comes with a full fledged dependency resolution library,
inspired by `Molinillo <https://github.com/CocoaPods/Molinillo>`__.

Why?
----

Packaging system and dependency management in Python is rather
convoluted and hard to understand for newcomers. Even for seasoned
developers it might be cumbersome at times to create all files needed in
a Python project: ``setup.py``, ``requirements.txt``, ``setup.cfg``,
``MANIFEST.in`` and the newly added ``Pipfile``.

So I wanted a tool that would limit everything to a single configuration
file to do: dependency management, packaging and publishing.

It takes inspiration in tools that exist in other languages, like
``composer`` (PHP) or ``cargo`` (Rust).

And, finally, there is no reliable tool to properly resolves
dependencies in Python, so I started ``poetry`` to bring an exhaustive
depency resolver to the Python community.

What about Pipenv?
~~~~~~~~~~~~~~~~~~

In short: I do not like the CLI it provides, or some of the decisions
made, and I think we can do a better and more intuitive one.

Also it only solves partially one problem: dependency management while I
wanted something more global and accurate to manage Python projects with
just one tool.

The ``Pipfile`` is just a replacement from ``requirements.txt`` but in
the end you will still need to populate your ``setup.py`` file (or
``setup.cfg``) with the exact same dependencies you declared in your
``Pipfile``. So, in the end, you will still need to manage a few
configuration files to properly setup your project.

Commands
--------

new
~~~

This command will help you kickstart your new Python project by creating
a directory structure suitable for most projects.

.. code:: bash

    poetry new my-package

will create a folder as follows:

.. code:: text

    my-project
    ├── poetry.toml
    ├── README.rst
    ├── my_project
        └── __init__.py
    ├── tests
        ├── __init__.py
        └── test_my_package

If you want to name your project differently than the folder, you can
pass the ``--name`` option:

.. code:: bash

    poetry new my-folder --my-package

install
~~~~~~~

The ``install`` command reads the ``poetry.toml`` file from the current
directory, resolves the dependencies, and installs them.

.. code:: bash

    poetry install

If there is a ``poetry.lock`` file in the current directory, it will use
the exact versions from there instead of resolving them. This ensures
that everyone using the library will get the same versions of the
dependencies.

If there is no ``poetry.lock`` file, Poetry will create one after
dependency resolution.

You can specify to the command that you do not want the development
dependencies installed by passing the ``--no-dev`` option.

.. code:: bash

    poetry install --no-dev

You can also specify the features you want installed by passing the
``--f|--features`` option (See `Features <#features>`__ for more info)

.. code:: bash

    poetry install --features "mysql pgsql"
    poetry install -f mysql -f pgsql

Options
^^^^^^^

-  ``--no-dev``: Do not install dev dependencies.
-  ``-f|--features``: Features to install (multiple values allowed).

update
~~~~~~

In order to get the latest versions of the dependencies and to update
the ``poetry.lock`` file, you should use the ``update`` command.

.. code:: bash

    poetry update

This will resolve all dependencies of the project and write the exact
versions into ``poetry.lock``.

If you just want to update a few packages and not all, you can list them
as such:

.. code:: bash

    poetry update requests toml

Options
^^^^^^^

-  ``--no-progress``: Removes the progress display that can mess with
   some terminals or scripts which don't handle backspace characters.

add
~~~

The ``add`` command adds required packages to your ``poetry.toml`` and
installs them.

If you do not specify a version constraint, poetry will choose a
suitable one based on the available package versions.

.. code:: bash

    poetry add requests pendulum

Options
^^^^^^^

-  ``--D|dev``: Add package as development dependency.
-  ``--optional`` : Add as an optional dependency.

remove
~~~~~~

The ``remove`` command removes a package from the current list of
installed packages

.. code:: bash

    poetry remove pendulum

Options
^^^^^^^

-  ``--D|dev``: Removes a package from the development dependencies.
-  ``--dry-run`` : Outputs the operations but will not execute anything
   (implicitly enables --verbose).

package
~~~~~~~

The ``package`` command builds the source and wheels archives.

Options
^^^^^^^

-  ``--no-universal``: Do not build a universal wheel.
-  ``--no-wheels``: Build only the source package.
-  ``-c|--clean``: Make a clean package.

publish
~~~~~~~

This command builds (if not already built) and publishes the package to
the remote repository.

It will automatically register the package before uploading if this is
the first time it is submitted.

Options
^^^^^^^

-  ``-r|--repository``: The repository to register the package to
   (default: ``pypi``). Should match a section of your ``~/.pypirc``
   file.

search
~~~~~~

This command searches for packages on a remote index.

.. code:: bash

    poetry search requests pendulum

Options
^^^^^^^

-  ``-N|--only-name``: Search only in name.

lock
~~~~

This command locks (without installing) the dependencies specified in
``poetry.toml``.

.. code:: bash

    poetry lock

The ``poetry.toml`` file
------------------------

A ``poetry.toml`` file is composed of multiple sections.

package
~~~~~~~

This section describes the specifics of the package

name
^^^^

The name of the package. **Required**

version
^^^^^^^

The version of the package. **Required**

This should follow `semantic versioning <http://semver.org/>`__. However
it will not be enforced and you remain free to follow another
specification.

python-version
^^^^^^^^^^^^^^

A list of Python versions for which the package is compatible.
**Required**

description
^^^^^^^^^^^

A short description of the package. **Required**

license
^^^^^^^

The license of the package.

The recommended notation for the most common licenses is (alphabetical):

-  Apache-2.0
-  BSD-2-Clause
-  BSD-3-Clause
-  BSD-4-Clause
-  GPL-2.0
-  GPL-2.0+
-  GPL-3.0
-  GPL-3.0+
-  LGPL-2.1
-  LGPL-2.1+
-  LGPL-3.0
-  LGPL-3.0+
-  MIT

Optional, but it is highly recommended to supply this. More identifiers
are listed at the `SPDX Open Source License
Registry <https://www.spdx.org/licenses/>`__.

authors
^^^^^^^

The authors of the package. This is a list of authors and should contain
at least one author.

Authors must be in the form ``name <email>``.

readme
^^^^^^

The readme file of the package. **Required**

The file can be either ``README.rst`` or ``README.md``. If it's a
markdown file you have to install the
`pandoc <https://github.com/jgm/pandoc>`__ utility so that it can be
automatically converted to a RestructuredText file.

You also need to have the
`pypandoc <https://pypi.python.org/pypi/pypandoc/>`__ package installed.
If you install ``poet`` via ``pip`` you can use the ``markdown-readme``
extra to do so.

.. code:: bash

    pip install pypoet[markdown-readme]

homepage
^^^^^^^^

An URL to the website of the project. **Optional**

repository
^^^^^^^^^^

An URL to the repository of the project. **Optional**

documentation
^^^^^^^^^^^^^

An URL to the documentation of the project. **Optional**

keywords
^^^^^^^^

A list of keywords (max: 5) that the package is related to. **Optional**

include and exclude
^^^^^^^^^^^^^^^^^^^

A list of patterns that will be included in the final package.

You can explicitly specify to Poet that a set of globs should be ignored
or included for the purposes of packaging. The globs specified in the
exclude field identify a set of files that are not included when a
package is built.

If a VCS is being used for a package, the exclude field will be seeded
with the VCS’ ignore settings (``.gitignore`` for git for example).

.. code:: toml

    [package]
    # ...
    include = ["package/**/*.py", "package/**/.c"]

.. code:: toml

    exclude = ["package/excluded.py"]

If you packages lies elsewhere (say in a ``src`` directory), you can
tell ``poet`` to find them from there:

.. code:: toml

    include = { from = 'src', include = '**/*' }

Similarly, you can tell that the ``src`` directory represent the ``foo``
package:

.. code:: toml

    include = { from = 'src', include = '**/*', as = 'foo' }

``dependencies`` and ``dev-dependencies``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Poet is configured to look for dependencies on
`PyPi <https://pypi.org>`__ by default. Only the name and a version
string are required in this case.

.. code:: toml

    [dependencies]
    requests = "^2.13.0"

If you want to use a private repository, you can add it to your
``poetry.toml`` file, like so:

.. code:: toml

    [[source]]
    name = 'private'
    url = 'http://example.com/simple'

Caret requirement
^^^^^^^^^^^^^^^^^

**Caret requirements** allow SemVer compatible updates to a specified
version. An update is allowed if the new version number does not modify
the left-most non-zero digit in the major, minor, patch grouping. In
this case, if we ran ``poet update requests``, poet would update us to
version ``2.14.0`` if it was available, but would not update us to
``3.0.0``. If instead we had specified the version string as
``^0.1.13``, poet would update to ``0.1.14`` but not ``0.2.0``.
``0.0.x`` is not considered compatible with any other version.

Here are some more examples of caret requirements and the versions that
would be allowed with them:

.. code:: text

    ^1.2.3 := >=1.2.3 <2.0.0
    ^1.2 := >=1.2.0 <2.0.0
    ^1 := >=1.0.0 <2.0.0
    ^0.2.3 := >=0.2.3 <0.3.0
    ^0.0.3 := >=0.0.3 <0.0.4
    ^0.0 := >=0.0.0 <0.1.0
    ^0 := >=0.0.0 <1.0.0

Tilde requirements
^^^^^^^^^^^^^^^^^^

**Tilde requirements** specify a minimal version with some ability to
update. If you specify a major, minor, and patch version or only a major
and minor version, only patch-level changes are allowed. If you only
specify a major version, then minor- and patch-level changes are
allowed.

``~1.2.3`` is an example of a tilde requirement.

.. code:: text

    ~1.2.3 := >=1.2.3 <1.3.0
    ~1.2 := >=1.2.0 <1.3.0
    ~1 := >=1.0.0 <2.0.0

Wildcard requirements
^^^^^^^^^^^^^^^^^^^^^

**Wildcard requirements** allow for any version where the wildcard is
positioned.

``*``, ``1.*`` and ``1.2.*`` are examples of wildcard requirements.

.. code:: text

    * := >=0.0.0
    1.* := >=1.0.0 <2.0.0
    1.2.* := >=1.2.0 <1.3.0

Inequality requirements
^^^^^^^^^^^^^^^^^^^^^^^

**Inequality requirements** allow manually specifying a version range or
an exact version to depend on.

Here are some examples of inequality requirements:

.. code:: text

    >= 1.2.0
    > 1
    < 2
    != 1.2.3

Multiple requirements
^^^^^^^^^^^^^^^^^^^^^

Multiple version requirements can also be separated with a comma, e.g.
``>= 1.2, < 1.5``.

``git`` dependencies
^^^^^^^^^^^^^^^^^^^^

To depend on a library located in a ``git`` repository, the minimum
information you need to specify is the location of the repository with
the git key:

.. code:: toml

    [dependencies]
    requests = { git = "https://github.com/requests/requests.git" }

Since we haven’t specified any other information, Poetry assumes that we
intend to use the latest commit on the ``master`` branch to build our
project. You can combine the ``git`` key with the ``rev``, ``tag``, or
``branch`` keys to specify something else. Here's an example of
specifying that you want to use the latest commit on a branch named
``next``:

.. code:: toml

    [dependencies]
    requests = { git = "https://github.com/kennethreitz/requests.git", branch = "next" }

Python restricted dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also specify that a dependency should be installed only for
specific Python versions:

.. code:: toml

    [dependencies]
    pathlib2 = { version = "^2.2", python-versions = "~2.7" }

.. code:: toml

    [dependencies]
    pathlib2 = { version = "^2.2", python-versions = ["~2.7", "^3.2"] }

``scripts``
~~~~~~~~~~~

This section describe the scripts or executable that will be installed
when installing the package

.. code:: toml

    [scripts]
    poetry = 'poetry:console.run'

Here, we will have the ``poetry`` script installed which will execute
``console.run`` in the ``poetry`` package.

``features``
~~~~~~~~~~~~

Poetry supports features to allow expression of:

-  optional dependencies, which enhance a package, but are not required;
   and
-  clusters of optional dependencies.

.. code:: toml

    [package]
    name = "awesome"

    [features]
    mysql = ["mysqlclient"]
    pgsql = ["psycopg2"]

    [dependencies]
    # These packages are mandatory and form the core of this package’s distribution.
    mandatory = "^1.0"

    # A list of all of the optional dependencies, some of which are included in the
    # above `features`. They can be opted into by apps.
    psycopg2 = { version = "^2.7", optional = true }
    mysqlclient = { version = "^1.3", optional = true }

When installing packages, you can specify features by using the
``-f|--features`` option:

.. code:: bash

    poet install --features "mysql pgsql"
    poet install -f mysql -f pgsql

``plugins``
~~~~~~~~~~~

Poetry supports arbitrary plugins wich work similarly to `setuptools
entry
points <http://setuptools.readthedocs.io/en/latest/setuptools.html>`__.
To match the example in the setuptools documentation, you would use the
following:

.. code:: toml

    [plugins] # Optional super table

    [plugins."blogtool.parsers"]
    ".rst" = "some_module::SomeClass"

Resources
---------

-  `Official Website <https://poetry.eustace.io>`__
-  `Issue Tracker <https://github.com/sdispater/poetry/issues>`__


