from client_python.main import main
from security import vault
def test_main():
    main()
def test_key():
    key1 = vault.get_or_create_communication_key()
    print(len(key1))
    key2 = vault.get_or_create_communication_key()
    print(key1 == key2)
