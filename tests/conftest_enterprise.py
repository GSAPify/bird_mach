"""Enterprise test configuration."""
import pytest

@pytest.fixture
def admin_user():
    return {'id': 'admin', 'role': 'admin'}

@pytest.fixture
def test_project():
    return {'id': 'proj-1', 'name': 'Test'}
