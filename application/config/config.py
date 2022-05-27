import os, logging
from datetime import datetime, timedelta

app = {
    'ENV': 'development', # 'production'
    'DEBUG': True,
    'TESTING': False,
    'PROPAGATE_EXCEPTIONS': None,
    'PRESERVE_CONTEXT_ON_EXCEPTION': None,
    'TRAP_HTTP_EXCEPTIONS': False,
    'TRAP_BAD_REQUEST_ERRORS': None,
    'SECRET_KEY': None, # $ python -c "import secrets; print(secrets.token_hex())"
    'SESSION_COOKIE_NAME': 'session',
    'SESSION_COOKIE_DOMAIN': None,
    'SESSION_COOKIE_PATH': None,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SECURE': False,
    'SESSION_COOKIE_SAMESITE': None,
    'PERMANENT_SESSION_LIFETIME': timedelta(days=31),
    'SESSION_REFRESH_EACH_REQUEST': True,
    'USE_X_SENDFILE': False,
    'SEND_FILE_MAX_AGE_DEFAULT': None,
    'SERVER_NAME': None,
    'APPLICATION_ROOT': '/',
    'PREFERRED_URL_SCHEME': 'http',
    'MAX_CONTENT_LENGTH': None,
    'JSON_AS_ASCII': True,
    'JSON_SORT_KEYS': True,
    'JSONIFY_PRETTYPRINT_REGULAR': False,
    'JSONIFY_MIMETYPE': 'application/json',
    'TEMPLATES_AUTO_RELOAD': None,
    'EXPLAIN_TEMPLATE_LOADING': False,
    'MAX_COOKIE_SIZE': 4093
}

config = {
    'ENCRYPTION_SALT': '[YOURT_SALT_KEY]',
    'UPLOAD_PATH': os.path.join('[UPLOAD_PATH]'),
    'XSS_FILTER': True,
    'SESSION_NAME': 'session',
    'SESSION_PATH': os.path.join('application', 'sessions'),
    'SESSION_EXPIRE': timedelta(days=30)
}

database = {
    'host': "[HOST]",
    'port': "[PORT]",
    'user': "[USER]",
    'password': "[PASSWORD]",
    'database': "[DATABASE]",
    'dbdriver': "[DBDRIVER]",
    'driver': "[DRIVER]",
    'autocommit': True,
    'buffered': True,
}

log = {
    'LOG_PATH': os.path.join('application', 'logs'),
    'LOG_NAME': datetime.now().strftime('log-%Y-%m-%d.log'),
    'LOG_LEVEL': logging.DEBUG,
    'LOG_FORMAT': logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
}