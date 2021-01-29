from app.encoders import jsonable_encoder
from app.db_models import User
from app.security import get_password_hash, verify_password


class CRUDUser:
    @classmethod
    def get(cls, db, *, id):
        return db.query(User).filter(User.id == id).first()

    @classmethod
    def get_by_email(cls, db, *, email):
        return db.query(User).filter(User.email == email).first()

    @classmethod
    def get_multi(cls, db, *, limit=100, skip=0):
        return db.query(User).offset(skip).limit(limit).all()

    @classmethod
    def create(cls, db, *, user_in):
        db_obj = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update(cls, db, *, user, user_in):
        obj_data = jsonable_encoder(user)
        if isinstance(user_in, dict):
            update_data = user_in
        else:
            update_data = user_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        for field in obj_data:
            if field in update_data:
                setattr(user, field, update_data[field])

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def delete(cls, db, *, id):
        obj = db.query(User).get(id)
        db.delete(obj)
        db.commit()
        return obj

    @classmethod
    def count(cls, db):
        return db.query(User).count()

    @classmethod
    def authenticate(cls, db, *, email: str, password: str):
        user = cls.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
