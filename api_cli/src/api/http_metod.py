from enum import Enum


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    PATCH = "PATCH"
