from datetime import datetime
from pyriver.db import db


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        modify_date = self.modify_date
        try:
            self.modify_date = datetime.utcnow()
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            # TODO: logging!
            print("EXCEPTION:", e)
        self.modify_date = modify_date
        return False
