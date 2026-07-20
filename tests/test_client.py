from client_python.client import main,Joueur
import os
import pytest


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Requires graphical environment"
)
def test_main():
    main()
def test_classJoueur():
    joueur=Joueur()
    joueur._initialiser_stats()
