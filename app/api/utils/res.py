from flask import jsonify


# 返回信息
def res(status: int, code: int, msg: str, data=None):
    base = {"code": code, "msg": msg}
    if data is None:
        response = jsonify(base=base)
    else:
        response = jsonify(base=base, data=data)
    response.status_code = status

    return response
