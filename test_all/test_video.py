import faker
import pytest
from werkzeug.datastructures import FileStorage
from .conftest import Login
Fake = faker.Faker('zh_CN')


class TestVideo(object):
    # 正常发布视频
    def test_publish(self, client):
        user = Login(client, 'abcdf', '123456')
        file = FileStorage(stream=open('test.mp4', 'rb'), filename='test.mp4')
        response = client.post(
            '/video/publish',
            data={'data': file,
                  'title': 'test video',
                  'description': 'test description'},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == 'success'

    # 无标题投稿
    def test_publish_without_title(self, client):
        user = Login(client, 'abcdf', '123456')
        file = FileStorage(stream=open('test.mp4', 'rb'), filename='test.mp4')
        response = client.post(
            '/video/publish',
            data={'data': file,
                  'description': 'test description'},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == 'success'

    # 文件格式错误
    def test_publish_wrong_file(self, client):
        user = Login(client, 'abcdf', '123456')
        file = FileStorage(stream=open('./test.txt', 'rb'), filename='test.txt')
        response = client.post(
            '/video/publish',
            data={'data': file,
                  'title': 'test video',
                  'description': 'test description'},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '文件格式错误'

    # 标题为空
    def test_publish_space_title(self, client):
        user = Login(client, 'abcdf', '123456')
        file = FileStorage(stream=open('test.mp4', 'rb'), filename='test.mp4')
        response = client.post(
            '/video/publish',
            data={'data': file,
                  'title': '',
                  'description': 'test description'},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '标题为空'

    # 获取首页视频流
    def test_feed(self, client):
        latest_time = int(Fake.past_datetime(start_date='-30m').timestamp())
        response = client.get('/video/feed/', query_string={'latest_time': str(latest_time)})
        assert response.status_code == 200
        assert response.json['base']['code'] == 200

        assert 'items' in response.json['data']
        key_list = ["id", "user_id", "title", "description", "video_url", "cover_url",
                    "created_at", "updated_at", "deleted_at", "visit_count", "like_count", "comment_count"]

        for item in response.json['data']['items']:
            for key in key_list:
                assert key in item.keys()

    # 获取首页视频流(无时间)
    def test_feed_without_time(self, client):
        response = client.get('/video/feed/')
        assert response.status_code == 200
        assert response.json['base']['code'] == 200

        assert 'items' in response.json['data']
        key_list = ["id", "user_id", "title", "description", "video_url", "cover_url",
                    "created_at", "updated_at", "deleted_at", "visit_count", "like_count", "comment_count"]

        for item in response.json['data']['items']:
            for key in key_list:
                assert key in item.keys()

    # 发布列表
    @pytest.mark.parametrize("num,size", [(1, 1), (2, 10), (8, 25), (9, 33), (34, 34)])
    def test_list(self, client, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/video/list',
            query_string={"user_id": user.data['id'],
                          "page_num": num,
                          "page_size": size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        assert 'total' in response.json['data']
        assert 'items' in response.json['data']
        key_list = ["id", "user_id", "title", "description", "video_url", "cover_url",
                    "created_at", "updated_at", "deleted_at", "visit_count", "like_count", "comment_count"]

        for item in response.json['data']['items']:
            for key in key_list:
                assert key in item.keys()

    # 发布列表(每页数据0错误)
    @pytest.mark.parametrize("num,size", [(1, 0), (2, 0), (1, -1), (-1, 5), (-5, 10)])
    def test_list_wrong_page(self, client, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/video/list',
            query_string={"user_id": user.data['id'],
                          "page_num": num,
                          "page_size": size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        if size <= 0:
            assert response.json['base']['msg'] == "单页尺寸必须大于0"
        if num < 0:
            assert response.json['base']['msg'] == "页码必须大于等于0"

    @pytest.mark.parametrize("uid", [1234124, 1451, 12415])
    def test_list_wrong_userid(self, client, uid):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/video/list',
            query_string={"user_id": uid,
                          "page_num": 2,
                          "page_size": 2},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == "该用户不存在"

    # 热门列表
    @pytest.mark.parametrize("num,size", [(1, 1), (2, 10), (8, 25), (9, 33), (34, 34)])
    def test_popular(self, client,  num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/video/popular',
            query_string={"page_num": num, "page_size": size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        print(response.json['base']['msg'])
        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        assert 'items' in response.json['data']
        key_list = ["id", "user_id", "title", "description", "video_url", "cover_url",
                    "created_at", "updated_at", "deleted_at", "visit_count", "like_count", "comment_count"]

        for item in response.json['data']['items']:
            for key in key_list:
                assert key in item.keys()

    @pytest.mark.parametrize("num,size", [(1, 0), (2, 0), (1, -1), (-1, 5), (-5, 10)])
    def test_popular_wrong_page(self, client, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/video/popular',
            query_string={"page_num": num, "page_size": size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        # print(response.json)
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        if size <= 0:
            assert response.json['base']['msg'] == "每页记录数必须大于0"
        if num < 0:
            assert response.json['base']['msg'] == "页码必须大于等于0"

    @pytest.mark.parametrize("num,size", [(1, 1), (2, 10), (8, 25), (9, 33), (34, 34),
                                          (1, 0), (2, 0), (1, -1), (-1, 5), (-5, 10)])
    def test_search(self, client, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/video/search',
            data={"keywords": Fake.pystr(),
                  "page_num": 0,
                  "page_size": 5,
                  "username": "a",
                  "from_date": 0,
                  "to_date": 1720934376
                  },
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        assert response.json['data']['total'] >= 0
