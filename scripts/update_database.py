from .database.update_python import update_python_database
from .database.update_docs import update_docs_database
from .database.update_security import update_security_database
from .database.update_rust import update_rust_database
from .database.update_performance import update_performance_database


def main():

    update_python_database()

    update_docs_database()

    update_security_database()

    


if __name__ == "__main__":
    main()

