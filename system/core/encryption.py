from passlib.hash import bcrypt, sha256_crypt, sha512_crypt, md5_crypt, sha1_crypt
from application.config import config

class Encryption():
    def __init__(self, schema: str = 'sha256'):
        '''
        `Encryption(schema: str = 'sha256')`

        method

        `crypt(word: str[, **options])`
        '''
        self.schema = schema

    def crypt(self, word: str, **options) -> str:
        '''
        `crypt(word: str[, **options])`

        `**options[salt: str, rounds: int, ident: str, truncate_error: bool, relaxed: bool, salt_size: int]`

        word를 암호화 한다.
        '''
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