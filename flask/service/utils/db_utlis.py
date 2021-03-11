import pymysql
from dbutils.pooled_db import PooledDB, SharedDBConnection


class SQLHelper(object):

    def __init__(self):
        # 创建数据库连接池
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=5,
            mincached=2,
            blocking=True,
            host='122.226.84.37',
            port=3306,
            user='root',
            password='meidi',
            database='cloud_customer_service',
            charset='utf8'
        )

    def connect(self):
        conn = self.pool.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    def disconnect(self, conn, cursor):
        cursor.close()
        conn.close()

    def fetchone(self, sql, params=None):
        """
        获取单条
        :param sql:
        :param params:
        :return:
        """
        if not params:
            params = []
        conn, cursor = self.connect()
        cursor.execute(sql, params)
        result = cursor.fetchone()
        self.disconnect(conn, cursor)
        return result

    def fetchall(self, sql, params=None):
        """
        获取所有
        :param sql:
        :param params:
        :return:
        """
        import pymysql
        if not params:
            params = []
        conn, cursor = self.connect()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        self.disconnect(conn, cursor)
        return result

    def commit(self, sql, params):
        """
        增删改
        :param sql:
        :param params:
        :return:
        """
        import pymysql
        if not params:
            params = []

        conn, cursor = self.connect()
        cursor.execute(sql, params)
        conn.commit()
        self.disconnect(conn, cursor)


db = SQLHelper()