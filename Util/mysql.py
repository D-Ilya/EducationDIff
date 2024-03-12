import pymysql
from .color import ColorPrint as cout
from .custom import decode_utf8


class MySql:

    def __init__(self, mysql_conf: dict):
        self.dbh = None
        try:
            self.connect(mysql_conf)
        except Exception as err:
            raise cout.print_err(f'FAILED: {err.args[1]}')

    def connect(self, config: dict):

        print(f"Connect to MySQL.{config['db']} - ", end='')
        self.dbh = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['pw'],
            port=config['port'],
            database=config['db'],
            cursorclass=pymysql.cursors.DictCursor
        )
        cout.print_ok('OK')

    def get_data(self, sql: str, params: tuple = None, pk: str = None):
        cursor = self.dbh.cursor()
        try:
            cursor.execute(sql, params) if params else cursor.execute(sql)
        except pymysql.InternalError as err:
            raise cout.print_err(err.args[1])
        except pymysql.DatabaseError as err:
            raise cout.print_err(err.args[1])
        data = cursor.fetchall()
        if not data:
            return None
        return self._convert_by_pk(data, pk) if pk else decode_utf8(data)

    def execute(self, sql: str, params: tuple = None):
        cursor = self.dbh.cursor()
        cursor.execute(sql, params) if params else cursor.execute(sql)
        self.dbh.commit()

    @staticmethod
    def _convert_by_pk(data: list, pk: str):
        return {item[pk]: item for item in decode_utf8(data)}
