import re


def username_sha(username) -> (str, bool):
    """
    用户名校验
    :param username:用户名
    :return:bool flag:True->合法，False->不合法
    :return:str msg:(错误)信息
    """
    msg = "success"
    flag = True

    ptn_username = r'^[a-zA-Z0-9\u4e00-\u9fa5]{1,10}$'
    if not re.match(ptn_username, username):
        msg = "用户名长度应在0-10个字符之间，且由中英文及数字组成"
        flag = False
    return msg, flag
