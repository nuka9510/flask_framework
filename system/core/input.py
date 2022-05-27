import html
from flask import request
from application.config import config

class Input():
    def __init__(self):
        '''
        method

        get(name: str[, **options])

        post(name: str[, **options])

        file(name: str[, **options])

        header(name: str)

        query_string()

        get_json()
        '''

    def get(self, name=None, default=None, action='store'):
        '''
        get(name: str[, **options])

        **options[default=: str|int|..., action: str]
        '''
        result = None

        if name:
            if action == 'append':
                result = request.args.getlist(name)

                for i in range(len(result)):
                    if type(result[i]) == str:
                        result[i] = html.escape(result[i]) if config['XSS_FILTER'] else result[i]
            elif action == 'store':
                result = request.args.get(name)

                if type(result) == str:
                    result = html.escape(result) if config['XSS_FILTER'] else result

                result = result if result else default
        else:
            result.request.args.to_dict()

        return result

    def post(self, name=None, default=None, action='store'):
        '''
        post(name: str[, **options])

        **options[default=: str|int|..., action: str]
        '''
        result = None

        if name:
            result = default

            if action == 'append':
                result = request.form.getlist(name)

                for i in range(len(result)):
                    if type(result[i]) == str:
                        result[i] = html.escape(result[i]) if config['XSS_FILTER'] else result[i]
            elif action == 'store':
                result = request.form.get(name)

                if type(result) == str:
                    result = html.escape(result) if config['XSS_FILTER'] else result

                result = result if result else default
        else:
            result = request.form.to_dict()

        return result

    def file(self, name=None, action='store'):
        '''
        file(name)
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

    def header(self, name=None):
        '''
        header(name: str)
        '''
        result = None

        if name:
            result = request.headers.get(name)
        else:
            result = request.headers

        return result

    def query_string(self):
        '''
        query_string()
        '''
        return request.query_string.decode()

    def get_json(self):
        '''
        get_json()
        '''
        return request.get_json()