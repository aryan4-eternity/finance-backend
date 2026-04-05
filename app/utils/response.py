from typing import Any, Optional
def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> dict:
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return response
def error_response(message: str = "An error occurred", errors: Optional[list] = None) -> dict:
    response = {"success": False, "message": message}
    if errors:
        response["errors"] = errors
    return response