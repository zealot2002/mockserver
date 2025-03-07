def success(data=None, msg="ok"):
    """
    成功响应
    """
    return {
        'code': 1,
        'msg': msg,
        'data': data or {}
    }

def error(msg="error", data=None):
    """
    错误响应
    """
    return {
        'code': -1,
        'msg': msg,
        'data': data or {}
    } 