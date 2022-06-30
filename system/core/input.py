import html
from typing import Union, Type, Any
from flask import request
from application.config import config

class Input():
    def __init__(self):
        '''
        `Input()`

        method

        `get(name: str | None = None[, default: Any | None = None[, type: type | None = None[, action: str = 'store']]])`

        `post(name: str | None = None[, default: Any | None = None[, type: type | None = None[, action: str = 'store']]])`

        `file(name: str | None = None[, action: str='store'])`

        `header(name: str | None = None)`

        `query_string()`

        `get_json()`
        '''

    def get(self, name: Union[str, None] = None, default: Union[Any, None] = None, type: Union[Type[Any], None] = None, action: str = 'store'):
        '''
        `get(name: str | None = None[, default: Any | None = None[, type: type | None = None[, action: str = 'store']]])`
        
        get으로 받아온 데이터를 return 한다.
        '''
        result = None

        if name:
            if action == 'append':
                result = request.args.getlist(name, type)

                for i in range(len(result)):
                    if (type == str \
                        or not type) \
                        and result[i]:
                        result[i] = html.escape(result[i]) if config['XSS_FILTER'] else result[i]
            elif action == 'store':
                result = request.args.get(name, default, type)

                if (type == str \
                    or not type) \
                    and result:
                    result = html.escape(result) if config['XSS_FILTER'] else result
        else:
            result = request.args.to_dict()

        return result

    def post(self, name: Union[str, None] = None, default: Union[Any, None] = None, type: Union[Type[Any], None] = None, action: str = 'store'):
        '''
        `post(name: str | None = None[, default: Any | None = None[, type: type | None = None[, action: str = 'store']]])`
        
        post로 받아온 데이터를 return 한다.
        '''
        result = None

        if name:
            if action == 'append':
                result = request.form.getlist(name, type)

                for i in range(len(result)):
                    if (type == str \
                        or not type) \
                        and result[i]:
                        result[i] = html.escape(result[i]) if config['XSS_FILTER'] else result[i]
            elif action == 'store':
                result = request.form.get(name, default, type)

                if (type == str \
                    or not type) \
                    and result:
                    result = html.escape(result) if config['XSS_FILTER'] else result
        else:
            result = request.form.to_dict()

        return result

    def file(self, name: Union[str, None] = None, action: str = 'store'):
        '''
        `file(name: str | None = None[, action: str = 'store'])`
        
        multipart/form-data로 받아온 데이터를 return 한다.
        '''
        result = None
        
        if name:
            if action == 'append':
                result = request.files.getlist(name)
            else:
                result = request.files.get(name)
        else:
            result = request.files.to_dict()
        
        return result

    def header(self, name: Union[str, None] = None):
        '''
        `header(name: str | None = None)`
        
        header로 받아온 데이터를 return 한다.
        '''
        result = None

        if name:
            result = request.headers.get(name)
        else:
            result = request.headers

        return result

    def query_string(self) -> str:
        '''
        `query_string()`

        query string을 return 한다.
        '''
        return request.query_string.decode()

    def get_json(self):
        '''
        `get_json()`

        applcation/json으로 받아온 데이터를 return 한다.
        '''
        return request.get_json()