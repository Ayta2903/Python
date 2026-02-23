import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models import Student, Subject, Grade


class TestStudentCRUD:

    def test_create_student(self, db_session):
        timestamp = datetime.now().timestamp()
        unique_email = f"Иванова Айталина.{timestamp} ayta@mail.ru"

        # Создаем нового студента
        student = Student(
            name="Иванова Айталина",
            email=unique_email,
            age=33
        )

        db_session.add(student)
        db_session.commit()
        student_id = student.id

        saved_student = db_session.query(Student).filter_by(email=unique_email).first()
        assert saved_student is not None
        assert saved_student.name == "Иванова Айталина"
        assert saved_student.age == 33
        assert saved_student.email == unique_email

        print(f"✅ Создан студент: {saved_student.name} (ID: {saved_student.id})")

        db_session.delete(saved_student)
        db_session.commit()

        # Проверяем очистку
        assert db_session.query(Student).filter_by(email=unique_email).first() is None
        print(f"Студент удален")

    def test_update_student(self, db_session):
        timestamp = datetime.now().timestamp()
        unique_email = f"update.test.{timestamp}@example.com"
        student = Student(
            name="Студент 789",
            email=unique_email,
            age=20
        )
        db_session.add(student)
        db_session.commit()

        student_id = student.id
        print(f"Создан студент для обновления (ID: {student_id})")

        student.name = "Студент 555"
        student.age = 21
        db_session.commit()

        updated_student = db_session.query(Student).get(student_id)
        assert updated_student.name == "Студент 555"
        assert updated_student.age == 21
        assert updated_student.email == unique_email

        print(f"Студент обновлен: {updated_student.name}, возраст: {updated_student.age}")

        db_session.delete(updated_student)
        db_session.commit()
        print(f"Студент удален")

    def test_delete_student(self, db_session):
        timestamp = datetime.now().timestamp()
        unique_email = f"Студент для удаления{timestamp}почта@почта"
        student = Student(
            name="Студент для удаления",
            email=unique_email,
            age=25
        )
        db_session.add(student)
        db_session.commit()

        student_id = student.id
        print(f"Создан студент для удаления (ID: {student_id})")

        assert db_session.query(Student).get(student_id) is not None

        db_session.delete(student)
        db_session.commit()

        assert db_session.query(Student).get(student_id) is None
        print(f"Студент успешно удален")


class TestSubjectCRUD:

    def test_create_subject(self, db_session):
        timestamp = datetime.now().timestamp()
        unique_name = f"Математика {timestamp}"

        subject = Subject(
            name=unique_name,
            description="Высшая математика",
            credits=4
        )

        db_session.add(subject)
        db_session.commit()
        subject_id = subject.id

        saved_subject = db_session.query(Subject).filter_by(name=unique_name).first()
        assert saved_subject is not None
        assert saved_subject.name == unique_name
        assert saved_subject.description == "Высшая математика"
        assert saved_subject.credits == 4

        print(f"Создан предмет: {saved_subject.name} (ID: {saved_subject.id})")

        db_session.delete(saved_subject)
        db_session.commit()

        assert db_session.query(Subject).get(subject_id) is None
        print(f"Предмет удален")

    def test_update_subject(self, db_session):
        timestamp = datetime.now().timestamp()
        unique_name = f"Физика {timestamp}"
        subject = Subject(
            name=unique_name,
            description="Основы физики",
            credits=3
        )
        db_session.add(subject)
        db_session.commit()

        subject_id = subject.id
        print(f"Создан предмет для обновления (ID: {subject_id})")

        subject.description = "Продвинутая физика"
        subject.credits = 5
        db_session.commit()

        updated_subject = db_session.query(Subject).get(subject_id)
        assert updated_subject.description == "Продвинутая физика"
        assert updated_subject.credits == 5
        assert updated_subject.name == unique_name  # Название не должно измениться

        print(f"Предмет обновлен: {updated_subject.credits} кредитов")

        db_session.delete(updated_subject)
        db_session.commit()
        print(f"Предмет удален")

    def test_delete_subject(self, db_session):
        """Тест удаления предмета"""
        # Создаем предмет для удаления
        timestamp = datetime.now().timestamp()
        unique_name = f"Химия {timestamp}"
        subject = Subject(
            name=unique_name,
            description="Химия",
            credits=3
        )
        db_session.add(subject)
        db_session.commit()

        subject_id = subject.id
        print(f"✅ Создан предмет для удаления (ID: {subject_id})")

        # Проверяем, что предмет существует
        assert db_session.query(Subject).get(subject_id) is not None

        # Удаляем предмет
        db_session.delete(subject)
        db_session.commit()

        # Проверяем удаление
        assert db_session.query(Subject).get(subject_id) is None
        print(f"✅ Предмет успешно удален")

class TestGradeCRUD:

    def test_create_grade(self, db_session, test_student, test_subject):
        grade = Grade(
            student_id=test_student.id,
            subject_id=test_subject.id,
            grade=4
        )

        db_session.add(grade)
        db_session.commit()

        grade_id = grade.id

        saved_grade = db_session.query(Grade).get(grade_id)
        assert saved_grade is not None
        assert saved_grade.student_id == test_student.id
        assert saved_grade.subject_id == test_subject.id
        assert saved_grade.grade == 4

        print(f"Создана оценка {saved_grade.grade} для студента {test_student.name} по предмету {test_subject.name}")

        db_session.delete(saved_grade)
        db_session.commit()

        assert db_session.query(Grade).get(grade_id) is None
        print(f"Оценка удалена")

    def test_update_grade(self, db_session, test_student, test_subject):
        grade = Grade(
            student_id=test_student.id,
            subject_id=test_subject.id,
            grade=3
        )
        db_session.add(grade)
        db_session.commit()

        grade_id = grade.id
        print(f"Создана оценка {grade.grade} (ID: {grade_id})")

        # Обновляем оценку
        grade.grade = 5
        db_session.commit()

        updated_grade = db_session.query(Grade).get(grade_id)
        assert updated_grade.grade == 5
        assert updated_grade.student_id == test_student.id
        assert updated_grade.subject_id == test_subject.id

        print(f"Оценка обновлена: {updated_grade.grade}")

        db_session.delete(updated_grade)
        db_session.commit()
        print(f"Оценка удалена")

    def test_delete_grade(self, db_session, test_student, test_subject):
        grade = Grade(
            student_id=test_student.id,
            subject_id=test_subject.id,
            grade=3
        )
        db_session.add(grade)
        db_session.commit()

        grade_id = grade.id
        print(f"Создана оценка для удаления (ID: {grade_id})")

        assert db_session.query(Grade).get(grade_id) is not None

        db_session.delete(grade)
        db_session.commit()

        assert db_session.query(Grade).get(grade_id) is None
        print(f"Оценка успешно удалена")


class TestEdgeCases:

    def test_unique_email_constraint(self, db_session):
        timestamp = datetime.now().timestamp()
        email = f"Студент 145{timestamp}@pochta.com"

        student1 = Student(name="Студент 1", email=email, age=20)
        db_session.add(student1)
        db_session.commit()
        print(f"Создан первый студент с email: {email}")

        student2 = Student(name="Студент 2", email=email, age=22)
        db_session.add(student2)

        with pytest.raises(IntegrityError) as excinfo:
            db_session.commit()
        print(f"Ожидаемо получена ошибка уникальности: {type(excinfo.value).__name__}")

        db_session.rollback()

        db_session.delete(student1)
        db_session.commit()
        print(f"Тестовые данные очищены")

    def test_unique_subject_name_constraint(self, db_session):
        timestamp = datetime.now().timestamp()
        subject_name = f"Уникальный Предмет {timestamp}"

        subject1 = Subject(name=subject_name, description="Первый", credits=3)
        db_session.add(subject1)
        db_session.commit()
        print(f"Создан первый предмет: {subject_name}")

        subject2 = Subject(name=subject_name, description="Второй", credits=4)
        db_session.add(subject2)

        with pytest.raises(IntegrityError) as excinfo:
            db_session.commit()
        print(f"Ожидаемо получена ошибка уникальности: {type(excinfo.value).__name__}")

        db_session.rollback()

        db_session.delete(subject1)
        db_session.commit()
        print(f"Тестовые данные очищены")