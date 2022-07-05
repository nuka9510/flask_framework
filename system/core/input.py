import html
from typing import Optional, Union, Type, Any
from flask import request
from application.config import config

class Input():
    def __init__(self):
        '''
        `Input()`

        method

        `get(name: str | None = None[, default: Any | None = None[, type: type | None = None[, action: str = 'store'[, literal: list | tuple | set | None = None]]]])`

        `post(name: str | None = None[, default: Any | None = None[, type: type | None = None[, action: str = 'store'[, literal: list | tuple | set | None = None]]]])`

        `file(name: str | None = None[, action: str='store'])`

        `header(name: str | None = None)`

        `query_string()`

        `get_json()`
        '''

    def _convert(self, arg: Any, default: Optional[Any], type: Optional[Type[Any]], literal: Optional[Union[list, tuple, set]]):
        '''
        `_convert(arg: Any, default: Any | None, type: type | None, literal: list | tuple | set | None)`
        '''
        if (type == str or not type) \
            and arg:
            arg = html.escape(arg) if config['XSS_FILTER'] else arg

        if literal \
            and arg not in literal:
            arg = default

        return arg

    def get(self, name: Optional[str] = None, default: Optional[Any] = None, type: Optional[Type[Any]] = None, action: str = 'store', literal: Optional[Union[list, tuple, set]] = None):
        '''
        `get(name: str | None = None[, default: Any | None = None[, type: type | None = None[, action: str = 'store'[, literal: list | tuple | set | None = None]]]])`
        
        get으로 받아온 데이터를 return 한다.
        '''
        result = None

        if name:
            if action == 'append':
                result = request.args.getlist(name, type)

                for i in range(len(result)):
                    result[i] = self._convert(result[i], default, type, literal)
            elif action == 'store':
                result = request.args.get(name, default, type)
                result = self._convert(result, default, type, literal)
        else:
            result = request.args.to_dict()

        return result

    def post(self, name: Optional[str] = None, default: Optional[Any] = None, type: Optional[Type[Any]] = None, action: str = 'store', literal: Optional[Union[list, tuple, set]] = None):
        '''
        `post(name: str | None = None[, default: Any | None = None[, type: type | None = None[, action: str = 'store'[, literal: list | tuple | set | None = None]]]])`
        
        post로 받아온 데이터를 return 한다.
        '''
        result = None

        if name:
            if action == 'append':
                result = request.form.getlist(name, type)

                for i in range(len(result)):
                    result[i] = self._convert(result[i], default, type, literal)
            elif action == 'store':
                result = request.form.get(name, default, type)
                result = self._convert(result, default, type, literal)
        else:
            result = request.form.to_dict()

        return result

    def file(self, name: Optional[str] = None, action: str = 'store'):
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

    def header(self, name: Optional[str] = None):
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