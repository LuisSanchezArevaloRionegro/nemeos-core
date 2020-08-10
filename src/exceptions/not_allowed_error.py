from utils import APIException

class NotAllowedError(APIException):

    def __init__(self, message = "Not allowed", status_code=None, payload=None):
        APIException.__init__(self, message)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv