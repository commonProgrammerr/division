import pytest
from unittest.mock import patch
from sqlmodel import create_engine
from division import models


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    tmpdir = request.getfixturevalue("tmpdir")
    with tmpdir.as_cwd():
        yield


@pytest.fixture(autouse=True, scope="function")
def setup_testing_database(request):
    """For each test, create a database file on tmpdir
    force database.py to use that filepath.
    """

    if "no_test_db" in request.keywords:
        yield
        return

    tmpdir = request.getfixturevalue("tmpdir")
    test_db = str(tmpdir.join("database.test.db"))

    engine = create_engine(f"sqlite:///{test_db}")
    user.SQLModel.metadata.create_all(bind=engine)
    with patch("division.database.engine", engine):
        yield
