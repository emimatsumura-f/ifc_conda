from ifc_app.db import get_db
from datetime import datetime

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(id):
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()
        if not user:
            return None
        return User(user['id'], user['username'])

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class ConversionHistory:
    def __init__(self, id, user_id, filename, processed_date, element_count):
        self.id = id
        self.user_id = user_id
        self.filename = filename
        self.processed_date = processed_date
        self.element_count = element_count

    @staticmethod
    def create(user_id, filename, element_count):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO conversion_history (user_id, filename, processed_date, element_count) VALUES (?, ?, ?, ?)',
            (user_id, filename, datetime.now(), element_count)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_user_history(user_id):
        db = get_db()
        history = db.execute(
            'SELECT * FROM conversion_history WHERE user_id = ? ORDER BY processed_date DESC',
            (user_id,)
        ).fetchall()
        return history

    @staticmethod
    def get_by_id(id):
        db = get_db()
        history = db.execute(
            'SELECT * FROM conversion_history WHERE id = ?',
            (id,)
        ).fetchone()
        if history is None:
            return None
        return ConversionHistory(
            history['id'],
            history['user_id'],
            history['filename'],
            history['processed_date'],
            history['element_count']
        )

    @staticmethod
    def delete(id, user_id):
        db = get_db()
        # ユーザーIDを確認して、自分の履歴のみ削除可能
        result = db.execute(
            'DELETE FROM conversion_history WHERE id = ? AND user_id = ?',
            (id, user_id)
        )
        db.commit()
        return result.rowcount > 0  # 削除が成功したかどうかを返す