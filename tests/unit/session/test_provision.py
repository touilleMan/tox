import sys

import pytest

from tox.exception import MissingRequirement


@pytest.fixture(scope="session")
def next_tox_major():
    """a tox version we can guarantee to not be available"""
    return "10.0.0"


def test_provision_min_version_is_requires(newconfig, next_tox_major):
    with pytest.raises(MissingRequirement) as context:
        newconfig(
            [],
            """
            [tox]
            minversion = {}
        """.format(
                next_tox_major
            ),
        )
    config = context.value.config

    deps = [r.name for r in config.envconfigs[config.provision_tox_env].deps]
    assert deps == ["tox >= {}".format(next_tox_major)]
    assert config.run_provision is True
    assert config.toxworkdir
    assert config.toxinipath
    assert config.provision_tox_env == ".tox"
    assert config.ignore_basepython_conflict is False


def test_provision_tox_change_name(newconfig):
    config = newconfig(
        [],
        """
        [tox]
        provision_tox_env = magic
    """,
    )
    assert config.provision_tox_env == "magic"


def test_provision_basepython_global_only(newconfig, next_tox_major):
    """we don't want to inherit basepython from global"""
    with pytest.raises(MissingRequirement) as context:
        newconfig(
            [],
            """
            [tox]
            minversion = {}
            [testenv]
            basepython = what
        """.format(
                next_tox_major
            ),
        )
    config = context.value.config
    base_python = config.envconfigs[".tox"].basepython
    assert base_python == sys.executable


def test_provision_basepython_local(newconfig, next_tox_major):
    """however adhere to basepython when explicilty set"""
    with pytest.raises(MissingRequirement) as context:
        newconfig(
            [],
            """
            [tox]
            minversion = {}
            [testenv:.tox]
            basepython = what
        """.format(
                next_tox_major
            ),
        )
    config = context.value.config
    base_python = config.envconfigs[".tox"].basepython
    assert base_python == "what"
