from client_python.main import main
import os
import pytest


@pytest.mark.skipif(
    os.getenv("GITHUB_WORKFLOW") == "Python CI Report
    ",
    reason="Ignoré dans le workflow Python car pas de serveur"
)
def test_main():
    main()

