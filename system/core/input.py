import html
from typing import Optional, Union, Type, Any
from flask import request
from application.config import config

class Input():
    def __init__(self):
        '''
        `Input()`

        ```
        @method get(name: str | None = None, default: Any | None = None, type: type | None = None, action: str = 'store', literal: list | tuple | set | None = None) -> (List | Any | Dict[str, str] | None)
        @method post(name: str | None = None, default: Any | None = None, type: type | None = None, action: str = 'store', literal: list | tuple | set | None = None) -> (List | Any | Dict[str, str] | None)
        @method file(name: str | None = None, action: str='store') -> (List[FileStorage] | FileStorage | Dict[str, FileStorage] | None)
        @method header(name: str | None = None) ->  -> (str | Headers | None)
        @method query_string() -> str
        @method get_json() -> (Any | None)
        ```
        '''

    def _convert(self, arg: Any, default: Optional[Any], type: Optional[Type[Any]], literal: Optional[Union[list, tuple, set]]):
        '''
        XSS_FILTER 적용, literal 확인 및 defualt 값 셋팅
        ```
        @param {Any} arg - 처리할 데이터
        @param {Any | None} default - default 값
        @param {type} type - 데이터의 type
        @param {list | tuple | set | None} literal - 확인할 literal 값
        @returns
        ```
        '''
        if (type == str or not type):
            if arg:
                arg = html.escape(arg) if config['XSS_FILTER'] else arg

            if not arg:
                arg = None

        if literal \
            and arg not in literal:
            arg = None

        if arg == None:
            arg = default

        return arg

    def get(self, name: Optional[str] = None, default: Optional[Any] = None, type: Optional[Type[Any]] = None, action: str = 'store', literal: Optional[Union[list, tuple, set]] = None):
        '''
        get으로 받아온 데이터를 return 한다.
        ```
        @param {str | None} [name=None] - 받아온 데이터의 name
        @param {Any | None} [default=None] - 데이터가 없을 시 넣어 줄 default 값
        @param {type | None} [type=None] - 데이터의 type
        @param {str} [action='store'] - 데이터를 받아오는 방식에 대한 값
        @param {list | tuple | set | None} [literal=None] - 받아야할 데이터에 대한 literal
        @returns
        ```
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
            result = request.args.to_dict(False)

        return result

    def post(self, name: Optional[str] = None, default: Optional[Any] = None, type: Optional[Type[Any]] = None, action: str = 'store', literal: Optional[Union[list, tuple, set]] = None):
        '''
        post로 받아온 데이터를 return 한다.
        ```
        @param {str | None} [name=None] - 받아온 데이터의 name
        @param {Any | None} [default=None] - 데이터가 없을 시 넣어 줄 default 값
        @param {type | None} [type=None] - 데이터의 type
        @param {str} [action='store'] - 데이터를 받아오는 방식에 대한 값
        @param {list | tuple | set | None} [literal=None] - 받아야할 데이터에 대한 literal
        @returns
        ```
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
            result = request.form.to_dict(False)

        return result

    def file(self, name: Optional[str] = None, action: str = 'store'):
        '''
        multipart/form-data로 받아온 데이터를 return 한다.
        ```
        @param {str | None} [name=None] - 받아온 데이터의 name
        @param {str} [action='store'] - 데이터를 받아오는 방식에 대한 값
        @returns
        ```
        '''
        result = None
        
        if name:
            if action == 'append':
                result = request.files.getlist(name)
            else:
                result = request.files.get(name)
        else:
            result = request.files.to_dict(False)
        
        return result

    def header(self, name: Optional[str] = None):
        '''
        header로 받아온 데이터를 return 한다.
        ```
        @param {str | None} [name=None] - 받아온 데이터의 name
        @returns
        ```
        '''
        result = None

        if name:
            result = request.headers.get(name)
        else:
            result = request.headers

        return result

    def query_string(self) -> str:
        '''
        query string을 return 한다.
        ```
        @returns
        ```
        '''
        return request.query_string.decode()

    def get_json(self):
        '''
        applcation/json으로 받아온 데이터를 return 한다.
        ```
        @returns
        ```
        '''
        return request.get_json()