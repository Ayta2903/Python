from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, text, inspect
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(name='{self.name}', email='{self.email}')>"


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(200))
    credits = Column(Integer, default=3)

    grades = relationship("Grade", back_populates="subject", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subject(name='{self.name}', credits={self.credits})>"


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    grade = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

    def __repr__(self):
        return f"<Grade(student_id={self.student_id}, subject_id={self.subject_id}, grade={self.grade})>"


def init_db(engine):
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        Base.metadata.create_all(engine)

        created_tables = [table for table in ['students', 'subjects', 'grades']
                          if table not in existing_tables]

        if created_tables:
            print(f"Созданы новые таблицы: {', '.join(created_tables)}")
        else:
            print("Все необходимые таблицы уже существуют")

    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")