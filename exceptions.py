class VkUserAuthFailed(Exception):
    def __init__(self, message):
        self.message = 'You have not access to API service'
        super().__init__(f'{self.message}, {message.strip()}')


class UploadPhotoError(Exception):
    def __init__(self, message):
        self.message = 'The photo did not upload to the server'
        super().__init__(f'{self.message}, {message.strip()}')


class SavePhotoError(Exception):
    def __init__(self, message):
        self.message = 'The photo did not save on the server'
        super().__init__(f'{self.message}, {message.strip()}')


class PostWallImgError(Exception):
    def __init__(self, message):
        self.message = 'The photo did not post on the wall'
        super().__init__(f'{self.message}, {message.strip()}')
