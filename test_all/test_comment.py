import faker
import pytest
from .conftest import Login

Fake = faker.Faker('Zh-CN')


class TestComment(object):
    # 发表评论
    @pytest.mark.parametrize('video_id,comment_id', [('1', '0'), ('10', ''), ('', '1'), ('', '2')])
    def test_publish(self, client, video_id, comment_id):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/comment/publish',
            data={'video_id': video_id,
                  'comment_id': comment_id,
                  'content': Fake.pystr(min_chars=5, max_chars=50)},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        if response.status_code != 200:
            print(response.json['base']['msg'])
        assert response.status_code == 200
        assert response.json['base']['code'] == 200

    # 视频id与评论id同时为空
    def test_publish_with_empty_id(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/comment/publish',
            data={'video_id': '',
                  'comment_id': '',
                  'content': Fake.pystr(min_chars=5, max_chars=50)},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200

    # 内容为空
    def test_publish_with_empty_content(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/comment/publish',
            data={'video_id': '1',
                  'comment_id': '',
                  'content': ''},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200

    # 视频不存在
    def test_publish_with_wrong_video_id(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/comment/publish',
            data={'video_id': '1000',
                  'comment_id': '',
                  'content': '1'},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200

    # 评论不存在
    def test_publish_with_wrong_comment_id(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/comment/publish',
            data={'video_id': '',
                  'comment_id': '1000',
                  'content': '1'},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200

    # 获取评论列表
    @pytest.mark.parametrize('video_id,comment_id,num,size',
                             [('1', '', 1, 1),
                              ('5', '', 5, 1),
                              ('', '1', 0, 1),
                              ('', '9', 5, 5)])
    def test_list(self, client, video_id, comment_id, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/comment/list',
            query_string={'video_id': video_id,
                          'comment_id': comment_id,
                          'page_num': num,
                          'page_size': size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        assert 'items' in response.json['data']

    @pytest.mark.parametrize('video_id,comment_id', [('1', ''), ('5', ''), ('', '1'), ('', '9')])
    def test_list_without_page(self, client, video_id, comment_id):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/comment/list',
            query_string={'video_id': video_id,
                          'comment_id': comment_id},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})
        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        assert 'items' in response.json['data']

    # 视频id与评论id同时为空
    def test_list_with_empty_id(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/comment/list',
            query_string={'video_id': '',
                          'comment_id': '',
                          'page_num': 1,
                          'page_size': 1},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '视频id与评论id不能同时为空'

    # 视频不存在
    def test_list_with_wrong_video_id(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/comment/list',
            query_string={'video_id': '1000',
                          'comment_id': '',
                          'page_num': 1,
                          'page_size': 1
                          },
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        # print(response.json)
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '该视频不存在'

    # 评论不存在
    def test_list_with_wrong_comment_id(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/comment/list',
            query_string={'video_id': '',
                          'comment_id': '1000',
                          'page_num': 1,
                          'page_size': 1},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '该评论不存在'

    # 页面数据错误
    @pytest.mark.parametrize('num,size', [(-1, 1), (-2, 5), (1, 0), (1, -6)])
    def test_list_with_wrong_page(self, client, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/comment/list',
            query_string={'video_id': '1',
                          'comment_id': '',
                          'page_num': num,
                          'page_size': size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        if num < 0:
            assert response.json['base']['msg'] == '页码必须大于等于0'
        if size < 0:
            assert response.json['base']['msg'] == '每页记录数必须大于0'

    # 删除评论
    @pytest.mark.parametrize('video_id,comment_id', [('1', ''), ('9', ''), ('', '5'), ('', '6')])
    def test_delete(self, client, video_id, comment_id):
        user = Login(client, 'abcdf', '123456')
        response = client.delete(
            '/comment/delete',
            data={'video_id': video_id,
                  'comment_id': comment_id},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == 'success'

    # 删除评论(视频id与评论id同时为空)
    def test_delete_with_empty_id(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.delete(
            '/comment/delete',
            data={'video_id': '',
                  'comment_id': ''},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '视频id和评论id不能同时为空'

    # 删除评论(视频id错误)
    @pytest.mark.parametrize('video_id', ['100', 'aacvb', '  a asdfa'])
    def test_delete_with_wrong_video_id(self, client, video_id):
        user = Login(client, 'abcdf', '123456')
        response = client.delete(
            '/comment/delete',
            data={'video_id': video_id,
                  'comment_id': ''},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '视频id错误'

    # 删除评论(评论id错误)
    @pytest.mark.parametrize('comment_id', ['435', 'aacvb', '  a asdfa'])
    def test_delete_with_wrong_comment_id(self, client, comment_id):
        user = Login(client, 'abcdf', '123456')
        response = client.delete(
            '/comment/delete',
            data={'video_id': '',
                  'comment_id': comment_id},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '评论id错误'
