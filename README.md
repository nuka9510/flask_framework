# flask_framework

## 사용 라이브러리 (*필수 설치)
* flask
  ```
  $ pip install -U Flask
  ```
* mysql-connector-python
  ```
  $ pip install mysql-connector-python
  ```
* pyodbc
  ```
  $ pip install pyodbc
  ```
* passlib
  ```
  $ pip install passlib
  ```

## Controller
* application/controllers/Example.py
  ```
  from system.core.controller import *

  bp = Blueprint('Example', __name__[, url_prefix='/example'])

  @bp.get('/')
  def get(self):
      return {'message': 'Example Page GET'}

  @bp.post('/')
  def post(self):
      return {'message': 'Example Page POST'}

  @bp.put('/')
  def put(self):
      return {'message': 'Example Page PUT'}

  @bp.delete('/')
  def delete(self):
      return {'message': 'Example Page DELETE'}
  ```
* application/controllers/\__init__.py
  ```
  from . import Example as Example
  ```
* app.py
  ```
  from application.controlers import Example

  app.register_blueprint(Example.bp)
  ```

## Model
* application/models/Example_Model.py
  ```
  from system import Model

  class Example_Model(Model):
      def __init__(self):
          super().__init__()

      def example(self):
          sql = '''[QUERY]'''

          self.execute(sql)
          res = self.fetchall()
          self.close()
          return res
  ```
* application/models/\__init__.py
  ```
  from .Example_Model import Example_Model as Example_Model
  ```
* application/controllers/Example.py
  ```
  from models import Example_Model

  example_model = Example_Model()
  ```
### query 실행
  ```
  self.execute(sql[, *data, ...])
  ```
### query 결과
  ```
  self.fetchall()
  or
  self.fetchone()
  or
  self.insert_id()
  ```
### db 연결 해제
  ```
  self.close()
  ```

## Util
* application/utils/Example_Util.py
  ```
  class Example_Util():
    [UTIL_METHOD]
  ```
* application/utils/\__init__.py
  ```
  from .Example_Util import Example_Util as Example_Util
  ```
###
  ```
  from application.utils import Example_Util

  util = Example_Util()

  util.[UTIL_METHOD]
  ```

## Input
  ```
  from system import Input

  input = Input()

  input.get(name[, **options])
  input.post(name[, **options])
  input.file(name[, **options])
  input.header(name)
  input.query_string()
  input.get_json()
  ```

## Upload
  ```
  from system import Upload

  upload = Upload()

  upload.file_upload(file[, *allowed_extensions][, **options])
  ```
### 파일 업로드
  ```
  upload.file_upload(file[, *allowed_extensions][, **options])
  ```
  * return
  ```
  {
    'result': True, // bool
    'file_name': 'file_name.jpg', // string
    'file_size': 0, // int
    'file_path': '/file_path', //string
    'full_path': '/file_path/file_name.jpg', // string
    'raw_name': 'file_name', // string
    'orig_name': 'file_name', // string
    'file_ext': '.jpg' // string
  }
  ```

## Encryption
  ```
  from system import Encryption

  encryption = Encryption([schema='sha256'])

  encryption.crypt(word[, **options])
  ```

## Logging
  ```
  from system import logger

  logger.debug(message)
  logger.info(message)
  logger.warning(message)
  logger.error(message)
  logger.critical(message)
  ```