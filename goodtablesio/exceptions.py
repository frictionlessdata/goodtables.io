# General


class GoodtablesioException(Exception):

    def __init__(self, message=None, code=None):

        super().__init__(message)

        self.code = code


# Validation

class InvalidJobConfiguration(GoodtablesioException):
    pass


class InvalidValidationConfiguration(GoodtablesioException):
    pass
