class AppException(Exception):
    status_code = 500
    detail = "Internal server error"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail


class NotFoundException(AppException):
    status_code = 404
    detail = "Resource not found"


class PermissionDeniedException(AppException):
    status_code = 403
    detail = "Permission denied"


class ConflictException(AppException):
    status_code = 409
    detail = "Conflict"


class UnauthorizedException(AppException):
    status_code = 401
    detail = "Unauthorized"


class WorkspaceNotFound(NotFoundException):
    detail = "Workspace not found"


class ProjectNotFound(NotFoundException):
    detail = "Project not found"


class TaskNotFound(NotFoundException):
    detail = "Task not found"


class WorkspacePermissionDenied(PermissionDeniedException):
    detail = "Workspace permission required"


class ProjectPermissionDenied(PermissionDeniedException):
    detail = "Project permission required"


class TaskPermissionDenied(PermissionDeniedException):
    detail = "Task permission required"


class AuthenticationFailed(UnauthorizedException):
    detail = "Invalid email or password"


class InvalidRefreshToken(UnauthorizedException):
    detail = "Invalid refresh token"


class EmailAlreadyExists(ConflictException):
    detail = "Email already exists"


class RefreshTokenNotFound(NotFoundException):
    detail = "Refresh token not found"


class UserNotFound(NotFoundException):
    detail = "User not found"
