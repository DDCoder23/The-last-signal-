from .database.update_python import update_python_database
from .database.update_docs import update_docs_database
from .database.update_security import update_security_database
from .database.update_rust import update_rust_database
from .database.update_performance import update_performance_database


def update_database():
    db = DatabaseManager()
    update_docs_database(db)

    update_python_database(db)

    

    update_security_database(db)
    update_rust_database(db)

    


if __name__ == "__main__":
    update_database()
    
