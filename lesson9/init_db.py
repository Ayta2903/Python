from sqlalchemy import create_engine, inspect, text
from models import Base

DB_URL = "postgresql://qa:skyqa@5.101.50.27:5432/x_clients"


def check_connection():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Успешное подключение к серверу 5.101.50.27")
        return engine
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None


def setup_database():
    print("Инициализация подключения к удаленной БД x_clients")

    engine = check_connection()
    if not engine:
        return False

    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        print(f"Существующие таблицы: {existing_tables}")

        Base.metadata.create_all(engine)

        new_inspector = inspect(engine)
        new_tables = new_inspector.get_table_names()
        created_tables = [t for t in ['students', 'subjects', 'grades'] if t in new_tables]

        print(f"Таблицы в базе данных x_clients: {created_tables}")
        print(f"Сервер: 5.101.50.27, База: x_clients")

    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        return False
    return True


def drop_test_tables(engine):
    try:
        Base.metadata.drop_all(engine)
        print("Все тестовые таблицы удалены")
    except Exception as e:
        print(f" Ошибка при удалении таблиц: {e}")


if __name__ == "__main__":
    setup_database()