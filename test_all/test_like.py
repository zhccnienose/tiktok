import pytest
from random import randint
from .conftest import Login


class TestLike(object):
    # 点赞视频
    @pytest.mark.parametrize('video_id,action_type',
                             [('1', '1'), ('1', '2'), ('4', '1'), ('4', '2'), ('20', '1'), ('20', '2')])
    def test_action_with_video_id(self, client, video_id, action_type):
        user = Login(client, 'abcdf', '123456')
        # print(user.data)
        response = client.post(
            '/like/action',
            data={'video_id': video_id,
                  'action_type': action_type},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 200
        assert response.json['base']['code'] == 200

    # 点赞评论
    @pytest.mark.parametrize('comment_id,action_type',
                             [('1', '1'), ('1', '2'), ('4', '1'), ('4', '2'), ('20', '1'), ('20', '2')])
    def test_action_with_comment_id(self, client, comment_id, action_type):
        user = Login(client, 'abcdf', '123456')
        # print(user.data)
        response = client.post(
            '/like/action',
            data={'comment_id': comment_id,
                  'action_type': action_type},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        # print(response.json['base']['msg'])
        assert response.status_code == 200
        assert response.json['base']['code'] == 200

    # id为空
    def test_action_without_id(self, client):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/like/action',
            data={'action_type': randint(1, 2)},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '视频id与评论id均为空'

    # 视频id错误
    @pytest.mark.parametrize('video_id,action_type',
                             [('100', '1'), ('100', '2'), ('412', '1'), ('412', '2')])
    def test_action_wrong_video_id(self, client, video_id, action_type):
        user = Login(client, 'abcdf', '123456')
        # print(user.data)
        response = client.post(
            '/like/action',
            data={'video_id': video_id,
                  'action_type': action_type},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '该视频不存在'

    # 评论id错误
    @pytest.mark.parametrize('comment_id,action_type',
                             [('100', '1'), ('100', '2'), ('412', '1'), ('412', '2')])
    def test_action_wrong_comment_id(self, client, comment_id, action_type):
        user = Login(client, 'abcdf', '123456')
        # print(user.data)
        response = client.post(
            '/like/action',
            data={'comment_id': comment_id,
                  'action_type': action_type},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '该评论不存在'

    # 操作类型错误
    @pytest.mark.parametrize('action_type', ['3', '6', '10', 'a'])
    def test_action_wrong_action_type(self, client, action_type):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/like/action',
            data={'video_id': '1',
                  'action_type': action_type},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200
        assert response.json['base']['msg'] == '操作类型错误'

    # 获取点赞列表
    @pytest.mark.parametrize("user_id,num,size", [('7193575627168026624', 1, 1),
                                                  ('7205298442124529664', 2, 10),
                                                  ('', 8, 25),
                                                  ('', 9, 33)])
    def test_list(self, client, user_id, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/like/list',
            query_string={'user_id': user_id,
                          'page_num': num,
                          'page_size': size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 200
        assert response.json['base']['code'] == 200

    @pytest.mark.parametrize("user_id,num,size", [('', -1, 1),
                                                  ('', 2, -10),
                                                  ('', 9, 0)])
    def test_list_with_wrong_page(self, client, user_id, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.get(
            '/like/list',
            query_string={'user_id': user_id,
                          'page_num': num,
                          'page_size': size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']})

        assert response.status_code == 422
        assert response.json['base']['code'] == 200
