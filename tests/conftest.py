import pytest
from website import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app



@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def clientloggedout(app):
    client.get('/logout')
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
