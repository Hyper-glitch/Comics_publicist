class BaseCustomException(Exception):
    def __init__(self, message):
        super().__init__(message)


class VkUserAuthFailed(BaseCustomException):
    def __init__(self, message):
        self.message = f'User authorization failed: no access_token passed, {message}'
        super().__init__(message)


class UploadPhotoError(BaseCustomException):
    pass


class SavePhotoError(BaseCustomException):
    pass
