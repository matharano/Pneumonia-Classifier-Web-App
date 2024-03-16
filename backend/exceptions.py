from fastapi import HTTPException
from http import HTTPStatus

class EmptyFile(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail='File is empty')

class UnsupportedFormat(HTTPException):
    def __init__(self, format:str) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST,
                         detail=f'File format not supported: {format}. Send an image in one of the following formats instead: png, jpg, or jpeg')
        
class BrokenImage(HTTPException):
    def __init__(self, size:int) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST,
                         detail=f'The file received was corrupted. Check the file and try again. Size received: {round(size / 10**6, 2)} MB')