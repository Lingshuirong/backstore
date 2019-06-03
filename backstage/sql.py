import pymysql
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
        try:
            conn, cursor = cls.open(cursor)
            if args:
                cursor.execute(sql, args[0])
            else:
                cursor.execute(sql)
            obj = cursor.fetchone()
            cls.close(conn, cursor)
            return obj
        except Exception as e:
            current_app.logger.error(e)
            return False

    @classmethod
    def fetch_all(cls, sql, *args, cursor=pymysql.cursors.DictCursor):
        try:
            conn, cursor = cls.open(cursor)
            if args:
                cursor.execute(sql, args[0])
                obj = cursor.fetchall()

                cls.close(conn, cursor)
                return obj
            else:
                cursor.execute(sql)
                obj = cursor.fetchall()
                if "sql_calc_found_rows" in sql:
                    cursor.execute("select found_rows() as total")
                    total = cursor.fetchone()
                else:
                    total = 0

                cls.close(conn, cursor)
                return obj, total
        except Exception as e:
            current_app.logger.error(e)
            return False

    @classmethod
    def execute(cls, sql, *args, cursor=pymysql.cursors.DictCursor):
        try:
            conn, cursor = cls.open(cursor)
            if args:
                cursor.execute(sql, args[0])
            else:
                cursor.execute(sql)
            cls.close(conn, cursor)
            return True
        except Exception as e:
            current_app.logger.error(e)
            return False

