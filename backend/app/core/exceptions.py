# backend/app/core/exceptions.py

class DetailedHTTPException(Exception):
    """
    Base class for custom HTTP exceptions that include a status code and detail.
    This allows for more structured error handling to be converted into FastAPI's HTTPException.
    """
    def __init__(self, status_code: int, detail: str, headers: dict | None = None):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
        super().__init__(detail)

class CredentialsException(DetailedHTTPException):
    def __init__(self, detail: str = "Could not validate credentials", headers: dict | None = None):
        super().__init__(status_code=401, detail=detail, headers=headers or {"WWW-Authenticate": "Bearer"})

class UserNotFoundException(DetailedHTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=404, detail=detail)

class EmailAlreadyExistsException(DetailedHTTPException):
    def __init__(self, detail: str = "Email already registered"):
        super().__init__(status_code=400, detail=detail) # Or 409 Conflict

class UsernameAlreadyExistsException(DetailedHTTPException):
    def __init__(self, detail: str = "Username already registered"):
        super().__init__(status_code=400, detail=detail) # Or 409 Conflict

class InvalidTokenException(DetailedHTTPException):
    def __init__(self, detail: str = "Invalid or expired token"):
        # Often associated with a 401, but could be 400 if the token format is wrong before validation
        super().__init__(status_code=401, detail=detail, headers={"WWW-Authenticate": "Bearer"})
        
class ExpiredSignatureError(InvalidTokenException): # Specific type of InvalidTokenException
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(detail=detail)

class SelfActionException(DetailedHTTPException):
    def __init__(self, detail: str = "User cannot perform this action on themselves"):
        super().__init__(status_code=400, detail=detail)
        
class ActionNotPermittedException(DetailedHTTPException):
    def __init__(self, detail: str = "Action not permitted"):
        super().__init__(status_code=403, detail=detail)


# Add more specific exceptions as needed, for example:
class EmailVerificationTokenInvalid(DetailedHTTPException):
    def __init__(self, detail: str = "Email verification token is invalid or has expired."):
        super().__init__(status_code=400, detail=detail)

class PasswordResetTokenInvalid(DetailedHTTPException):
    def __init__(self, detail: str = "Password reset token is invalid or has expired."):
        super().__init__(status_code=400, detail=detail)

class UserAlreadyVerifiedException(DetailedHTTPException):
    def __init__(self, detail: str = "User email is already verified."):
        super().__init__(status_code=400, detail=detail)
