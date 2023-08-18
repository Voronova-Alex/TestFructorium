from rest_framework.exceptions import ValidationError


class EmailVerificationException(ValidationError):
    default_detail = "non-local recipient verification failed"


class EmailAccountException(ValidationError):
    default_detail = "User with this email already exists"

class WrongOldPasswordException(ValidationError):
    default_detail = "Old password incorrect"
