import os, re
from application.config import config

class Upload():
    def __init__(self):
        '''
        method

        file_upload(file: fileobj[, *allowed_extensions: str][, **options])
        '''

    def file_upload(self, file, *allowed_extensions, **options):
        '''
        file_upload(file[, *allowed_extensions: str][, **options])

        *allowed_extensions['jpg', 'gif', 'png', ...]

        **options[upload_path: str, file_name: str]

        name으로 온 file을 upload한다.
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