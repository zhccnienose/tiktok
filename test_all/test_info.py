class TestInfo(object):
    # 获取用户信息
    def test_info(self, client):
        response = client.get(
            '/user/info',
            query_string={'user_id': '7205298442124529664'})
        assert response.status_code == 200
        assert response.json["base"]['code'] == 200
        assert response.json["data"]

    # 参数错误
    def test_wrong_info(self, client):
        response = client.get(
            '/user/info',
            query_string={'user_id': '72052984'},
        )
        assert response.status_code == 422
        assert response.json["base"]['code'] == 200
        assert response.json["base"]['msg'] == "该用户不存在"
        assert not response.json["data"]

    # 请求参数名错误
    def test_wrong_query_string(self, client):
        response = client.get(
            '/user/info',
            query_string={'userid': '72052984'},
        )
        assert response.status_code == 500
        assert response.json["base"]['code'] == 500
