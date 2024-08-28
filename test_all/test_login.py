from app.api.models import r
import pyotp


class TestLogin(object):
    # 登录
    def test_login(self, client):
        response = client.post(
            "/user/login",
            data={"username": "abcdef",
                  "password": "123456"}
        )
        assert response.status_code == 200
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "success"

    # mfa校验绑定后登录
    def test_login_with_code(self, client):
        hotp = pyotp.HOTP(r.get("7204528983432630272:secret").decode("utf-8"))
        code = hotp.at(int(r.get("7204528983432630272:login_num").decode("utf-8")))
        print(hotp.at(31))
        print(code)
        response = client.post(
            "/user/login",
            data={"username": "abcd",
                  "password": "123456",
                  "code": code}
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 200
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "success"

    # 用户名为空
    def test_login_space_username(self, client):
        response = client.post(
            "/user/login",
            data={"username": "",
                  "password": "123456",
                  }
        )
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "用户名不能为空"

    # 用户不存在
    def test_login_wrong_usenrame(self, client):
        response = client.post(
            "/user/login",
            data={"username": "abcdasdas",
                  "password": "1234",
                  }
        )
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "该用户不存在"

    # 密码为空
    def test_login_space_password(self, client):
        response = client.post(
            "/user/login",
            data={"username": "abcd",
                  "password": "",
                  }
        )
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "密码不能为空"

    # 密码错误
    def test_login_wrong_password(self, client):
        response = client.post(
            "/user/login",
            data={"username": "abcdf",
                  "password": "12",
                  }
        )
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "密码错误"

    # 校验码为空
    def test_login_space_code(self, client):
        response = client.post(
            "/user/login",
            data={"username": "abcd",
                  "password": "123456",
                  "code": ""
                  }
        )
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "校验码不能为空"

    # 校验码错误
    def test_login_wrong_code(self, client):
        response = client.post(
            "/user/login",
            data={"username": "abcd",
                  "password": "123456",
                  "code": "0"
                  }
        )
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "校验码错误"
