from client_python.main import main

def test_main():
    main()
def test_key():
    key1 = get_or_create_communication_key()
    print(len(key1))
    key2 = get_or_create_communication_key()
    print(key1 == key2)
