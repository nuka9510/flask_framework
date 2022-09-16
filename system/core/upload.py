import os, re
from werkzeug.datastructures import FileStorage
from application.config import config

class Upload():
    def __init__(self):
        '''
        `Upload()`

        ```
        @method file_upload(file: FileStorage, *allowed_extensions: str, **options) -> dict
        ```
        '''

    def file_upload(self, file: FileStorage, *allowed_extensions: str, **options) -> dict:
        '''
        file을 upload한다.
        ```
        @param {FileStorage} file - upload할 파일
        @param {str} *allowed_extensions - 허용할 확장자 'jpg', 'gif', 'png', ...
        @param {str} **options - upload 옵션
        @param {str} upload_path - options upload 경로
        @param {str} file_name - options 파일 명
        @returns 결과 값
        {
            'result': bool, upload 성공 여부
            'file_name': str, upload된 파일 명
            'file_size': int, 파일 용량
            'file_path': str, upload 경로
            'full_path': str, 파일 명을 포함한 upload 경로
            'raw_name': str, 확장자를 제외한 upload된 파일 명
            'orig_name': str, 파일 원본 명
            'file_ext': srt, 확장자
        }
        ```
        '''
        flag = False

        try:
            options['upload_path'] = os.path.join(config['UPLOAD_PATH'], options['upload_path'])
        except KeyError:
            options['upload_path'] = config['UPLOAD_PATH']

        if not os.path.exists(options['upload_path']):
            os.makedirs(options['upload_path'], mode=0o777)

        if allowed_extensions:
            extensions = set(allowed_extensions)

            flag = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in extensions
        else:
            flag = True
        
        if flag:
            orig_name = file.filename.rsplit('.', 1)[0]
            file_ext = f".{file.filename.rsplit('.', 1)[1].lower()}"

            try:
                options['file_name']
            except KeyError:
                options['file_name'] = orig_name

            full_path = os.path.join(options['upload_path'], f"{options['file_name']}{file_ext}")

            file.stream.seek(0, 2)

            file_size = file.stream.tell()

            file.stream.seek(0)

            file.save(full_path)

            return {
                'result': flag,
                'file_name': f"{options['file_name']}{file_ext}",
                'file_size': file_size,
                'file_path': '/'+re.sub(r'\\', '/', options['upload_path']),
                'full_path': '/'+re.sub(r'\\', '/', full_path),
                'raw_name': options['file_name'],
                'orig_name': orig_name,
                'file_ext': file_ext,
            }
        else:
            return {
                'result': flag
            }