import pymysql

from local_settings import dbconfig


def connect_mysql():
    """Возвращает соединение с MySQL с курсором в виде словаря."""
    try:
        with pymysql.connect(**dbconfig) as connection:
            with connection.cursor() as cursor:
                return cursor
    except pymysql.MySQLError as e:
        print(f"Connection error: {e}")
        return None
