class AppError(Exception):
    pass


class ApiError(AppError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class NetworkError(AppError):
    pass
