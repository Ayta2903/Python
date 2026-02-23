import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models import Base, Student, Subject, Grade
from datetime import datetime

DB_URL = "postgresql://qa:skyqa@5.101.50.27:5432/x_clients"


@pytest.fixture(scope="session")
def engine():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        Base.metadata.create_all(engine)
        print("Таблицы успешно созданы/проверены в базе 'x_clients'")

        return engine
    except OperationalError as e:
        pytest.skip(f"Невозможно подключиться к базе данных: {e}")
    except Exception as e:
        pytest.skip(f"Неожиданная ошибка: {e}")


@pytest.fixture(scope="function")
def db_session(engine):
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def test_student(db_session):
    """Создает тестового студента и очищает данные после теста"""
    timestamp = datetime.now().timestamp()
    student = Student(
        name="Тестовый Студент",
        email=f"test.student.{timestamp}@example.com",
        age=20
    )
    db_session.add(student)
    db_session.commit()

    yield student

    # Очистка данных
    try:
        db_session.delete(student)
        db_session.commit()
    except:
        db_session.rollback()


@pytest.fixture
def test_subject(db_session):
    timestamp = datetime.now().timestamp()
    subject = Subject(
        name=f"Тестовый Предмет {timestamp}",
        description="Тестовое описание",
        credits=3
    )
    db_session.add(subject)
    db_session.commit()

    yield subject

    try:
        db_session.delete(subject)
        db_session.commit()
    except:
        db_session.rollback()