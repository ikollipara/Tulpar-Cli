"""
tests/test_manage.py
Ian Kollipara
2022.04.05

Test Manage Command
"""
# Imports
from subprocess import CompletedProcess

from pytest import mark, raises
from typer import Exit
from typer.testing import CliRunner

from tulpar_cli import manage

runner = CliRunner()


@mark.parametrize("mod_name", ["black", "requests"])
def test_find_or_raise_successful(mod_name: str):
    """Test if find_or_raise will return None if an installed package is provided."""

    assert manage.find_or_raise(mod_name) is None


@mark.parametrize("mod_name", ["tulpar", "django"])
def test_find_or_raise_failure(mod_name: str):
    """Test if find_or_raise will raise an Exit if a package that is not installed."""

    with raises(Exit):
        manage.find_or_raise(mod_name)


def test_lint(mocker):
    """Test if the lint command runs correctly."""

    mocker.patch(
        "tulpar_cli.manage.run",
        return_value=CompletedProcess(["pylint", "."], 0, stdout="Pylint Ran"),
    )

    res = runner.invoke(manage.manage, ["lint"])

    assert res.exit_code == 0
    assert "Pylint Ran" in res.stdout


def test_lint_dry(mocker):
    """Test if the lint command doesn't run when --dry-run is active."""

    mocker.patch(
        "tulpar_cli.manage.run",
        return_value=CompletedProcess(["pylint", "."], 0, stdout="Pylint Ran"),
    )

    res = runner.invoke(manage.manage, ["lint", "--dry-run"])

    assert res.exit_code == 0
    assert not "Pylint Ran" in res.stdout


def test_format(mocker):
    """Test if the format command runs correctly."""

    mocker.patch(
        "tulpar_cli.manage.run",
        return_value=CompletedProcess(["black", "."], 0, stdout="Black Ran"),
    )

    res = runner.invoke(manage.manage, ["format"])

    assert res.exit_code == 0
    assert "Black Ran" in res.stdout


def test_format_dry(mocker):
    """Test if the format command doesn't run when --dry-run is active."""

    mocker.patch(
        "tulpar_cli.manage.run",
        return_value=CompletedProcess(["black", "."], 0, stdout="Black Ran"),
    )

    res = runner.invoke(manage.manage, ["format", "--dry-run"])

    assert res.exit_code == 0
    assert not "Black Ran" in res.stdout


def test_test(mocker):
    """Test if the test command runs correctly."""

    mocker.patch(
        "tulpar_cli.manage.run",
        return_value=CompletedProcess(["pytest"], 0, stdout="Pytest Ran"),
    )

    res = runner.invoke(manage.manage, "test")

    assert res.exit_code == 0
    assert "Pytest" in res.stdout


def test_audit(mocker):
    """Test if the audit command runs correctly."""

    mocker.patch(
        "tulpar_cli.manage.run",
        return_value=CompletedProcess(["bandit", "."], 0, stdout="Bandit Ran"),
    )

    res = runner.invoke(manage.manage, "audit")

    assert res.exit_code == 0
    assert "Bandit Ran" in res.stdout
