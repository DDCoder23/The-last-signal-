from update_python import update_python_database
from update_docs import update_docs_database
from update_security import update_security_database
from update_rust import update_rust_database
from update_performance import update_performance_database


def main():

    update_python_database()

    update_docs_database()

    update_security_database()

    


if __name__ == "__main__":
    main()

