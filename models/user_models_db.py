from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, String, Boolean, Integer

# from sqlalchemy.orm import declarative_base
from DB import session
from sqlalchemy import CheckConstraint

Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String, nullable=False)
    nit = Column(String, nullable=False)
    city = Column(String, nullable=False)
    department = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    password_confirm = Column(String, nullable=False)
    role = Column(
        String,
        nullable=False,
        # check_constraint="role IN ('Ingeniero', 'Tecnico', 'Profesional de salud')",
    )
    tos = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, correo='{self.email}')>"


def create_user(user_data):
    new_user = UserDB(
        # id=user_data.id,
        company=user_data.company,
        nit=user_data.nit,
        city=user_data.city,
        department=user_data.department,
        email=user_data.email,
        password=user_data.password,
        password_confirm=user_data.password_confirm,
        role=user_data.role,
        tos=user_data.tos,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_user_by_id(user_id: str):
    return session.query(UserDB).filter(UserDB.id == user_id).first()


def get_all_users():
    return session.query(UserDB).all()
