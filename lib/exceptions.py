from fastapi import HTTPException


class EntityNotFoundException(HTTPException):
    def __init__(self, detail: str = 'Entity'):
        super().__init__(
            detail={'error': f'{detail} does not exist'}, status_code=404)


class UniqueException(HTTPException):
    def __init__(self, entity: str = 'Entity'):
        super().__init__(
            detail={'error': f'{entity} already exists'}, status_code=409)


class DetailException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(detail={'error': detail}, status_code=404)


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail='Not authenticated')
