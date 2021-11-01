"""Nox sessions."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session

package = 'diglett'
locations = "src", "tests", "noxfile.py"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.
    """

    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.8")
def lint(session: Session) -> None:
    """Lint using flake8."""

    args = "src", "tests"
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python="3.7")
def quick_tests(session: Session) -> None:
    """Run the test suite for a single version of Python."""

    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", "--cov", external=True)


@nox.session(python=["3.10", "3.9", "3.8", "3.7"])
def tests(session: Session) -> None:
    """Run the test suite for multiple versions of Python."""

    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", "--cov", external=True)


@nox.session(python="3.8")
@nox.parametrize('pandas', ['1.0.4', '1.1.0', '1.2.0', '1.3.0'])
def tests_by_pandas(session: Session, pandas) -> None:
    """Run tests for various versions of pandas."""

    session.run("poetry", "add", f"pandas@{pandas}", external=True)

    # account for specific bug → https://github.com/numpy/numpy/issues/18355
    if pandas == '1.0.4':
        session.run("poetry", "add", "numpy@1.19.5", external=True)

    session.run("poetry", "install", external=True)
    session.run("poetry", "show", "pandas", external=True)
    session.run("poetry", "run", "pytest", "--cov", external=True)


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""

    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""

    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "sphinx", "sphinx-autodoc-typehints", "sphinx-book-theme")
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python="3.8")
def mypy(session: Session) -> None:
    """Type-check using mypy."""

    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python="3.8")
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""

    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("poetry", "run", "pytest", f"--typeguard-packages={package}", *args, external=True)


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
