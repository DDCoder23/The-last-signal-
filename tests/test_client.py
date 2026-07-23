from client_python.main import main
import os
import pytest


@pytest.mark.skipif(
    os.getenv("GITHUB_WORKFLOW") == "Python",
    reason="Ignoré dans le workflow Integration Tests"
)
def test_main():
    main()

