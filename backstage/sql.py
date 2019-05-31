import pymysql
# from flask.config import Config
from flask import current_app


class SqlHelper(object):
    @staticmethod
    def open(cursor):
        POOL = current_app.config['POOL']
        conn = POOL.connection()
        cursor = conn.cursor(cursor=cursor)
        return conn, cursor

    @staticmethod
    def close(conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def fetch_one(cls, sql, *args, cursor=pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        cursor.execute(sql, args[0])
        obj = cursor.fetchone()
        cls.close(conn, cursor)
        return obj

    @classmethod
    def fetch_all(cls, sql, *args, cursor=pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        cursor.execute(sql, args[0])
        obj = cursor.fetchall()
        cls.close(conn, cursor)

        return obj

    @classmethod
    def execute(cls, sql, *args, cursor=pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        cursor.execute(sql, args[0])
        cls.close(conn, cursor)


