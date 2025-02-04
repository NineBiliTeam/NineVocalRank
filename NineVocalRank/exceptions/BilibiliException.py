from http.client import HTTPException


class BilibiliException(HTTPException):
    pass


class BilibiliVideoException(BilibiliException):
    pass


class BilibiliPermissionException(BilibiliException):
    pass


class BilibiliRequestException(BilibiliException):
    pass
