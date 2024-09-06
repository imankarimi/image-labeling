from database import DB_CURSOR, DB_CONNECTION


class FilePath:
    @staticmethod
    def fetch():
        DB_CURSOR.execute("SELECT * FROM setting_file_path")
        res = DB_CURSOR.fetchall()
        return res

    @staticmethod
    def insert(file_path):
        DB_CURSOR.execute("INSERT INTO setting_file_path (file_path) VALUES (?)", (file_path,))
        res = DB_CONNECTION.commit()
        return res

    @staticmethod
    def bulk_insert():
        pass

    @staticmethod
    def update(pk, file_path):
        DB_CURSOR.execute("UPDATE setting_file_path SET file_path=? WHERE id=?", (file_path, pk))
        res = DB_CONNECTION.commit()
        return res

    @staticmethod
    def delete(data):
        for pk, file_path in data:
            DB_CURSOR.execute("DELETE FROM setting_file_path WHERE id=?", (pk,))
        DB_CONNECTION.commit()


class ImageLabel:
    def __init__(self, **kwargs):
        self.code = kwargs.get('code')
        self.name = kwargs.get('name')
        self.color_code = kwargs.get('color_code')

    @staticmethod
    def fetch():
        DB_CURSOR.execute("SELECT * FROM setting_labels")
        res = DB_CURSOR.fetchall()
        return res

    @staticmethod
    def insert():
        pass

    @staticmethod
    def bulk_insert(data):
        for label in data:
            DB_CURSOR.execute("INSERT INTO setting_labels (code, name, color_code) VALUES (?, ?, ?)", (label.code, label.name, label.color_code))
        res = DB_CONNECTION.commit()
        return res

    @staticmethod
    def delete(data):
        for pk, code, name, color in data:
            DB_CURSOR.execute("DELETE FROM setting_labels WHERE id=?", (pk,))
        DB_CONNECTION.commit()
