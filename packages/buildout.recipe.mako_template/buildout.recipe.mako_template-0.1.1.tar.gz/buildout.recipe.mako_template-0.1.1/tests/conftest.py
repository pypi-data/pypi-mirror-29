import pytest
import os
import os.path
import zc.buildout.testing
import zc.buildout.buildout
import distutils.dir_util
from buildout.recipe.mako_template import Recipe
from uuid import uuid4


@pytest.fixture(scope='function')
def work_dir(tmpdir):
    """Create a new directory and change execution context to it.

    As a tear-down return execution context to previous.
    """
    here = os.getcwd()
    tmpdirname = tmpdir.mkdir(uuid4().hex).strpath
    os.chdir(tmpdirname)
    try:
        yield tmpdirname
    finally:
        os.chdir(here)


@pytest.fixture
def buildout(work_dir):
    """Create and return a simple `buildout`instance."""
    buildout = zc.buildout.testing.Buildout()
    config = 'some config text\n'
    buildout['config'] = dict(contents=config)
    yield buildout


@pytest.fixture
def recipe(buildout):
    """Create and return `buildout.recipe instance`."""
    yield Recipe(buildout, 'config', buildout['config'])


@pytest.fixture
def buildout_dir(work_dir):
    """Preparer `buildout` configuration for acceptance testing.

    Copy `test/buildout` configuration into a new temporary directory and
    set execution context to it.
    Provide directory path.
    """
    buildout = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'buildout')
    distutils.dir_util.copy_tree(buildout, work_dir)
    path = os.path.join(work_dir, 'buildout.cfg')
    root = os.path.dirname((os.path.dirname(os.path.realpath(__file__))))
    with_fixed_path = open(path).read().replace('develop =', 'develop = ' + root)
    with open(path, 'w') as f:
        f.write(with_fixed_path)
    yield work_dir
