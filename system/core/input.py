import html
from typing import Optional, Union, Literal, Type, Any
from flask import request
from application.config import config

class Input():
    def _convert(self, arg: Any, default: Optional[Any], type: Optional[Type[Any]], literal: Optional[Union[list, tuple, set]]):
        '''XSS_FILTER 적용, literal 확인 및 defualt 값 셋팅
        ```
        Args:
            arg (Any): 처리할 데이터
            default (Optional[Any]): default 값
            type (Optional[Type[Any]]): 데이터의 type
            literal (Optional[Union[list, tuple, set]]): 확인할 literal 값

        Returns:
            Any: 처리된 데이터
        ```'''
        if (type == str or not type):
            if arg:
                arg = html.escape(arg) if config['XSS_FILTER'] else arg

            if not arg:
                arg = None

        if literal \
            and arg not in literal:
            arg = None

        if arg is None:
            arg = default

        return arg

    def get(self, name: Optional[str] = None, default: Optional[Any] = None, type: Optional[Type[Any]] = None, action: Literal['store', 'append'] = 'store', literal: Optional[Union[list, tuple, set]] = None):
        '''get으로 받아온 데이터를 return 한다.
        ```
        Args:
            name (Optional[str], optional): 받아온 데이터의 name. Defaults to None.
            default (Optional[Any], optional): 데이터가 없을 시 넣어 줄 default 값. Defaults to None.
            type (Optional[Type[Any]], optional): 데이터의 type. Defaults to None.
            action (Literal['store', 'append'], optional): 데이터를 받아오는 방식에 대한 값('store', 'append'). Defaults to 'store'.
            literal (Optional[Union[list, tuple, set]], optional): 받아야할 데이터에 대한 literal. Defaults to None.

        Returns:
            Union[list, Any, dict[str, list[str]], None]: 데이터
        ```'''
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

    def post(self, name: Optional[str] = None, default: Optional[Any] = None, type: Optional[Type[Any]] = None, action: Literal['store', 'append'] = 'store', literal: Optional[Union[list, tuple, set]] = None):
        '''post로 받아온 데이터를 return 한다.
        ```
        Args:
            name (Optional[str], optional): 받아온 데이터의 name. Defaults to None.
            default (Optional[Any], optional): 데이터가 없을 시 넣어 줄 default 값. Defaults to None.
            type (Optional[Type[Any]], optional): 데이터의 type. Defaults to None.
            action (Literal['store', 'append'], optional): 데이터를 받아오는 방식에 대한 값('store', 'append'). Defaults to 'store'.
            literal (Optional[Union[list, tuple, set]], optional): 받아야할 데이터에 대한 literal. Defaults to None.

        Returns:
            Union[list, Any, dict[str, list[str]], None]: 데이터
        ```'''
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

    def file(self, name: Optional[str] = None, action: Literal['store', 'append'] = 'store'):
        '''multipart/form-data로 받아온 file 데이터를 return 한다.
        ```
        Args:
            name (Optional[str], optional): 받아온 데이터의 name. Defaults to None.
            action (Literal['store', 'append'], optional): 데이터를 받아오는 방식에 대한 값('store', 'append'). Defaults to 'store'.

        Returns:
            Union[List[FileStorage], FileStorage, Dict[str, list[FileStorage]], None]: file 데이터
        ```'''
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
        '''header로 받아온 데이터를 return 한다.
        ```
        Args:
            name (Optional[str], optional): 받아온 데이터의 name. Defaults to None.

        Returns:
            Union[str, Headers, None]: header 데이터
        ```'''
        result = None

        if name:
            result = request.headers.get(name)
        else:
            result = request.headers

        return result

    def query_string(self) -> str:
        '''query string을 return 한다.
        ```
        Returns:
            str: query string
        ```'''
        return request.query_string.decode()

    def get_json(self):
        '''applcation/json으로 받아온 데이터를 return 한다.
        ```
        Returns:
            Any: json 데이터
        ```'''
        return request.get_json()