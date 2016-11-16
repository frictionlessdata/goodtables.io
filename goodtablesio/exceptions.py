# General

class GoodtablesioException(Exception):
    pass


# Validation

class InvalidJobConfiguration(GoodtablesioException):
    pass


class InvalidValidationConfiguration(GoodtablesioException):
    pass
