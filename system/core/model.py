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
        self.__connect()

    def __connect(self) -> None:
        '''
        `__connect()`

        database와 연결한다.
        '''
        try:
            if database['dbdriver'] == 'mysql':
                self.con = mysql.connector.connect(user=database['user'], password=database['password'], database=database['database'], host=database['host'], port=database['port'], autocommit=database['autocommit'], buffered=database['buffered'])
                self.cur = self.con.cursor()
            elif database['dbdriver'] == 'pyodbc':
                self.con = pyodbc.connect(f"DRIVER={{{database['driver']}}};SERVER={database['host']}{',' + database['port'] if database['port'] else ''};DATABASE={database['database']};UID={database['user']};PWD={database['password']}", autocommit=database['autocommit'])
                self.cur = self.con.cursor()
        except (mysql.connector.Error, pyodbc.Error) as err:
            logger.error(err)

    def __json_convert(self, value: Union[datetime.date, decimal.Decimal]) -> str:
        '''
        `__json_convert(self, value: datetime.date | decimal.Decimal)`

        json으로 변환이 가능 하도록 날짜와 실수 데이터를 문자열로 변환한다.
        '''
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, decimal.Decimal):
            return re.sub('\.$', '', re.sub('0+$', '', str(value)))
        else:
            return value

    def execute(self, sql: str, *data: Union[str, int]) -> bool:
        '''
        `execute(sql: str[, *data: str | int])`

        sql문을 실행시킨다.
        '''
        result = True

        try:
            if not data:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, data)
        except (mysql.connector.Error, pyodbc.Error) as err:
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
                    row.append(self.__json_convert(i))

                result.append(dict(zip(column_names, row)))
        elif database['dbdriver'] == 'pyodbc':
            for i in self.cur.fetchall():
                column_names = list()
                row = list()

                for j, k in enumerate(i.cursor_description):
                    column_names.append(k[0])
                    row.append(self.__json_convert(i[j]))

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
                    row.append(self.__json_convert(val))
            except TypeError:
                ''''''
        elif database['dbdriver'] == 'pyodbc':
            fetchone = self.cur.fetchone()

            try:
                for i, j in enumerate(fetchone.cursor_description):
                    column_names.append(j[0])
                    row.append(self.__json_convert(fetchone[i]))
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