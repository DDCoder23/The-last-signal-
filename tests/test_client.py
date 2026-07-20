from client_python.client import main
import os
import pytest


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Requires graphical environment"
)
def test_main():
    main()

