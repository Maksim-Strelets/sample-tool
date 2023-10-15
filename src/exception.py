class BaseError(Exception):
    pass


class ValidationError(BaseError):
    pass


class UrlNotValidException(ValidationError):
    pass


class FileNotValid(ValidationError):
    pass


class S3Error(BaseError):
    pass


class FileError(BaseError):
    pass
