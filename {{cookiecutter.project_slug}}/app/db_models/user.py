from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    def get_id(self):
        return self.id