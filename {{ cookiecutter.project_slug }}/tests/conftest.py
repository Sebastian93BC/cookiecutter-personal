import pytest
from pathlib import Path


@pytest.fixture
def project_root():
    """Return the project root directory (two levels up from tests/)."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def tmp_data(tmp_path):
    """Provide a temporary directory pre-populated with data subdirs."""
    for subdir in ("raw", "processed", "interim", "external"):
        (tmp_path / "data" / subdir).mkdir(parents=True)
    return tmp_path
