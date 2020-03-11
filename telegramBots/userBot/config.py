import base64
from io import BytesIO
from aiogram.types.input_file import InputFile

def bytes_to_str(bstr):
    '''convert any content to string representation'''
    return base64.b64encode(bstr).decode('utf-8')


def bytes_from_str(ustr):
    '''convert content back to bytes from string representation'''
    return base64.b64decode(ustr.encode('utf-8'))

def form_input_file(src: str) -> InputFile:
    tmp = BytesIO()
    tmp.write(bytes_from_str(src))
    tmp.seek(0)
    return InputFile(tmp)

