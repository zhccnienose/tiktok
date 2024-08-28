class TestRegiser(object):

    def test_register_space_username(self, client):
        response = client.post(
            "/user/register",
            data={"username": "",
                  "password": "adfasdf"})
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == '用户名为空'

    def test_register_used_username(self, client):
        response = client.post(
            "/user/register",
            data={"username": "abcd",
                  "password": "adfasdf"})
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == '该用户名已被使用'

    def test_register_space_password(self, client):
        response = client.post(
            "/user/register",
            data={"username": "12345678",
                  "password": ""})
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == '密码为空'

    def test_register_invalid_password(self, client):
        response = client.post(
            "/user/register",
            data={"username": "12345678",
                  "password": "123456789132456789123456713213213213213213213289123"})
        assert response.status_code == 422
        assert response.json["base"]["code"] == 200
        assert response.json["base"]["msg"] == "密码长度不能超过30个字符"
