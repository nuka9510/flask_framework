import mysql.connector, pyodbc, decimal, datetime, re
from typing import Union
from application.config import database
from system import logger

class Model():
    def __init__(self):
        '''
        `Model()`

        method

        `execute(sql: str[, *data: str | int])`

        `fetchall()`
        
        `fetchone()`

        `insert_id()`
        
        `close()`
        '''

    def __connect(self) -> None:
        '''
        `__connect()`

        database와 연결한다.
        '''
        try:
            if database['dbdriver'] == 'mysql':
                self.con = mysql.connector.connect(user=database['user'], password=database['password'], database=database['database'], host=database['host'], port=database['port'], autocommit=database['autocommit'], buffered=database['buffered'])
            elif database['dbdriver'] == 'pyodbc':
                self.con = pyodbc.connect(f"DRIVER={{{database['driver']}}};SERVER={database['host']}{',' + database['port'] if database['port'] else ''};DATABASE={database['database']};UID={database['user']};PWD={database['password']}", autocommit=database['autocommit'])

            self.cur = self.con.cursor()
            self.__connected = True
        except (mysql.connector.Error, pyodbc.Error) as err:
            logger.error(err)
            self.__connected = False

    def __convert(self, value: Union[datetime.date, decimal.Decimal]) -> str:
        '''
        `__convert(self, value: datetime.date | decimal.Decimal)`

        날짜 데이터를 '%Y-%m-%d %H:%M:%S' 형태의 문자열로 변환한다.

        실수 0은 정수로 변환한다.
        '''
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, decimal.Decimal) \
            and value == 0:
            return 0
        else:
            return value

    def execute(self, sql: str, *data: Union[str, int]) -> bool:
        '''
        `execute(sql: str[, *data: str | int])`

        sql문을 실행시킨다.
        '''
        result = True

        try:
            if not self.__connected:
                self.__connect()
        except AttributeError:
            self.__connect()

        try:
            if not data:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, data)
        except (mysql.connector.Error, pyodbc.Error) as err:
            logger.error(sql)

            if data:
                logger.error(data)

            logger.error(err)
            result = False

        return result

    def fetchall(self) -> list[dict]:
        '''
        `fetchall()`

        select된 모든 row를 불러온다.
        '''
        result = list()

        if database['dbdriver'] == 'mysql':
            column_names = self.cur.column_names

            for val in iter(self.cur.fetchall()):
                row = list()
                for i in val:
                    row.append(self.__convert(i))

                result.append(dict(zip(column_names, row)))
        elif database['dbdriver'] == 'pyodbc':
            for i in self.cur.fetchall():
                column_names = list()
                row = list()

                for j, k in enumerate(i.cursor_description):
                    column_names.append(k[0])
                    row.append(self.__convert(i[j]))

                result.append(dict(zip(column_names, row)))

        return result

    def fetchone(self) -> dict:
        '''
        `fetchone()`
        
        select된 row중 가장 첫 번째 row를 불러온다.
        '''
        column_names = list()
        row = list()

        if database['dbdriver'] == 'mysql':
            column_names = self.cur.column_names

            try:
                for val in self.cur.fetchone():
                    row.append(self.__convert(val))
            except TypeError:
                ''''''
        elif database['dbdriver'] == 'pyodbc':
            fetchone = self.cur.fetchone()

            try:
                for i, j in enumerate(fetchone.cursor_description):
                    column_names.append(j[0])
                    row.append(self.__convert(fetchone[i]))
            except AttributeError:
                ''''''

        return dict(zip(column_names, row))

    def insert_id(self) -> str:
        '''
        `insert_id()`

        가장 마지막으로 INSERT된 PRIMARY KEY 값을 불러온다.
        '''
        if database['dbdriver'] == 'mysql':
            return self.cur.lastrowid
        elif database['dbdriver'] == 'pyodbc':
            self.execute(f"SELECT @@IDENTITY AS id")
            return self.fetchone()['id']

    def close(self) -> None:
        '''
        `close()`

        database 연결을 끊는다.
        '''
        self.cur.close()
        self.con.close()
        self.__connected = False