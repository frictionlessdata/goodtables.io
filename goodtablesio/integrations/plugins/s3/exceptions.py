from goodtablesio import exceptions


class S3Exception(exceptions.GoodtablesioException):

    def __init__(self, message=None, code=None, operation=None):

        super().__init__(message, code)

        self.operation = operation
