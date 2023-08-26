from app.database import db


class BaseModelMethodsMixin:
    """
    Базовый клас для сохранения и удаления записи из БД
    """
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
