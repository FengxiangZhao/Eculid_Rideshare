# custom exceptions

class EmailVerificationException(Exception):
    # A general method describing the exceptions raised in the email verification
    pass

class EmailVerificationTokenExpired(EmailVerificationException):
    # The verification token is expired
    pass

class EmailVerificationTokenInvalid(EmailVerificationException):
    # the verification token is expired
    pass