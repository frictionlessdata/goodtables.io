# General

class GoodtablesioException(Exception):
    pass


# Validation

class InvalidTaskConfiguration(GoodtablesioException):
    pass


class InvalidTaskDescriptor(GoodtablesioException):
    pass
