from client_python.main import main
from security import vault
import pytest

def test_main():
    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    
def test_key():
    key1 = vault.get_or_create_communication_key()
    print(len(key1))
    key2 = vault.get_or_create_communication_key()
    print(key1 == key2)
