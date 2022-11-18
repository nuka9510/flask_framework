from typing import Union, Literal
from passlib.hash import bcrypt, sha256_crypt, sha512_crypt, md5_crypt, sha1_crypt
from application.config import config

class Encryption():
    def __init__(self, schema: Literal['bcrypt', 'sha256', 'sha512', 'md5', 'sha1'] = 'sha256'):
        '''암호화 Class
        ```
        Example:
            Encryption(schema='sha256')

        Args:
            schema (Literal['bcrypt', 'sha256', 'sha512', 'md5', 'sha1'], optional): 암호화 종류. Defaults to 'sha256'.
        ```'''
        self.schema = schema

    def crypt(self, word: str, **options: Union[str, int, bool]) -> str:
        '''word를 암호화 한다.
        ```
        Args:
            word (str): 암호화 할 문자열
            **options (Union[str, int, bool]): 암호화 옵션
                schema (Literal['bcrypt', 'sha256', 'sha512', 'md5', 'sha1'], optional): 암호화 종류
                salt (str, optional): salt 문자열. Defaults to config['ENCRYPTION_SALT'].
                rounds (int, optional): rounds 수('md5'는 예외)
                ident (str, optional): 'bcrypt'에서만 사용. Defaults to '2b'.
                truncate_error (bool, optional): 'bcrypt'에서만 사용. Defaults to False.
                relaxed (bool, optional): Defaults to False.
                salt_size (int, optional): ('md5', 'sha1')에서만 사용.Defaults to 8.

        Returns:
            str: 암화화 된 문자열
        ```'''
        try:
            self.schema = options['schema']
        except KeyError:
            pass
            
        try:
            options['salt']
        except KeyError:
            options['salt'] = config['ENCRYPTION_SALT']

        if self.schema == 'bcrypt':
            options['salt'] = options['salt'][0:22]

            try:
                options['rounds']
            except KeyError:
                options['rounds'] = 4
            
            try:
                options['ident']
            except KeyError:
                options['ident'] = '2b'
        
            try:
                options['truncate_error']
            except KeyError:
                options['truncate_error'] = False

            try:
                options['relaxed']
            except KeyError:
                options['relaxed'] = False
            
            return bcrypt.encrypt(bytes(word, 'utf-8'), **options)
        elif self.schema == 'sha256':
            options['salt'] = options['salt'][0:16]

            try:
                options['rounds']
            except KeyError:
                options['rounds'] = 1000

            try:
                options['relaxed']
            except KeyError:
                options['relaxed'] = False

            return sha256_crypt.encrypt(bytes(word, 'utf-8'), **options)
        elif self.schema == 'sha512':
            options['salt'] = options['salt'][0:16]

            try:
                options['rounds']
            except KeyError:
                options['rounds'] = 1000

            try:
                options['relaxed']
            except KeyError:
                options['relaxed'] = False

            return sha512_crypt.encrypt(bytes(word, 'utf-8'), **options)
        elif self.schema == 'md5':
            options['salt'] = options['salt'][0:8]

            try:
                options['salt_size']
            except KeyError:
                options['salt_size'] = 8

            try:
                options['relaxed']
            except KeyError:
                options['relaxed'] = False

            return md5_crypt.encrypt(bytes(word, 'utf-8'), **options)
        elif self.schema == 'sha1':
            options['salt'] = options['salt'][0:8]

            try:
                options['rounds']
            except KeyError:
                options['rounds'] = 480000

            try:
                options['salt_size']
            except KeyError:
                options['salt_size'] = 8

            try:
                options['relaxed']
            except KeyError:
                options['relaxed'] = False

            return sha1_crypt.encrypt(bytes(word, 'utf-8'), **options)