# webhook_sdk/utils/log_utils.py
def sanitize_data(data: dict) -> dict:
    """敏感信息脱敏"""
    safe_data = data.copy()
    redacted_fields = ["token", "password", "secret", "X-Token"]

    for field in redacted_fields:
        if field in safe_data:
            safe_data[field] = "***REDACTED***"

    return safe_data

def get_request_metadata(request) -> dict:
    """提取请求元数据"""
    return {
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "path": request.path
    }
