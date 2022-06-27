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

  bp = Blueprint('Example', __name__, url_prefix='/example')

  @bp.get('/')
  def get():
      return {'message': 'Example Page GET'}

  @bp.post('/')
  def post():
      return {'message': 'Example Page POST'}

  @bp.put('/')
  def put():
      return {'message': 'Example Page PUT'}

  @bp.delete('/')
  def delete():
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
  self.execute(sql: str[, *data: str | int])
  ```
### query 결과
  ```
  self.fetchall()
  ```
  ```
  self.fetchone()
  ```
  ```
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
  ```
  ```
  util.[UTIL_METHOD]
  ```

## Input
  ```
  from system import Input

  input = Input()
  ```
  ```
  input.get(name: str[, default: Any | None = None[, action: str = 'store']])
  ```
  ```
  input.post(name: str[, default: Any | None = None[, action: str = 'store']])
  ```
  ```
  input.file(name: str | None = None[, action: str='store'])
  ```
  ```
  input.header(name: str | None = None)
  ```
  ```
  input.query_string()
  ```
  ```
  input.get_json()
  ```

## Upload
  ```
  from system import Upload

  upload = Upload()
  ```
### 파일 업로드
  ```
  upload.file_upload(file: werkzeug.datastructures.FileStorage[, *allowed_extensions: str[, **options]])
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

  encryption = Encryption(schema: str = 'sha256')
  ```
  ```
  encryption.crypt(word: str[, **options])
  ```

## Logging
  ```
  from system import logger
  ```
  ```
  logger.debug(message: str)
  ```
  ```
  logger.info(message: str)
  ```
  ```
  logger.warning(message: str)
  ```
  ```
  logger.error(message: str)
  ```
  ```
  logger.critical(message: str)
  ```