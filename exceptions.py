class BaseCustomException(Exception):
    def __init__(self, message):
        super().__init__(message)


class VkUserAuthFailed(BaseCustomException):
    pass


class UploadPhotoError(BaseCustomException):
    pass


class SavePhotoError(BaseCustomException):
    pass
