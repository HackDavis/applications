from src.shared import Shared

db = Shared.db


class ModelUtils:
    @classmethod
    def drop_rows(cls):
        """Drop all rows from table"""
        db.session.query(cls).delete()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def insert_rows(cls, rows):
        """Insert provided rows into table"""
        db.session.add_all(rows)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
