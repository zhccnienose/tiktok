import pytest
from .conftest import Login


class TestInteract(object):
    # 关注,取消关注
    @pytest.mark.parametrize('to_user_id,action_type', [('7204528983432630272', 0),
                                                        ('7204528983432630272', 1),
                                                        ('7205298442124529664', 0),
                                                        ('7205298442124529664', 1)])
    def test_action(self, client, to_user_id, action_type):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/relation/action',
            data={'to_user_id': to_user_id,
                  'action_type': action_type},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        assert response.status_code == 200
        assert response.json['base']['code'] == 200

    # 关注,取消关注
    @pytest.mark.parametrize('to_user_id,action_type', [('7204528983432630272', 0),
                                                        ('7204528983432630272', 0),
                                                        ('7205298442124529664', 1),
                                                        ('7205298442124529664', 1)])
    def test_action_wrong_acton_type(self, client, to_user_id, action_type):
        flag = -1
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/relation/action',
            data={'to_user_id': to_user_id,
                  'action_type': action_type},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        if flag == action_type:
            assert response.status_code == 422
            assert response.json['base']['code'] == 200
            if not flag:
                assert response.json['base']['msg'] == '该用户已在关注列表中'
            else:
                assert response.json['base']['msg'] == '该用户不在关注列表中'

    # 关注列表
    @pytest.mark.parametrize('to_user_id,action_type,num,size', [('7204528983432630272', 0, 0, 5),
                                                                 ('7204528983432630272', 0, 1, 10),
                                                                 ('7204528983432630272', 0, 9, 34),
                                                                 ('7204528983432630272', 1, 0, 5),
                                                                 ('7204528983432630272', 1, 1, 10),
                                                                 ('7204528983432630272', 1, 9, 34)])
    def test_follow_list(self, client, to_user_id, action_type, num, size):
        user = Login(client, 'abcdf', '123456')
        response = client.post(
            '/relation/action',
            data={'to_user_id': to_user_id,
                  'action_type': action_type,
                  'page_num': num,
                  'page_size': size},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )

        response = client.get(
            '/following/list',
            query_string={'user_id': user.data['id']},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )
        assert response.status_code == 200
        assert response.json['base']['code'] == 200

        ids = [item['id'] for item in response.json['data']['items']]
        if action_type:
            assert to_user_id not in ids
        else:
            assert to_user_id in ids

    # 粉丝列表
    @pytest.mark.parametrize('to_user_id,action_type, num, size', [('7205298442124529664', 0, 0, 5),
                                                                   ('7205298442124529664', 0, 1, 10),
                                                                   ('7205298442124529664', 0, 9, 34),
                                                                   ('7205298442124529664', 1, 0, 5),
                                                                   ('7205298442124529664', 1, 1, 10),
                                                                   ('7205298442124529664', 1, 9, 34),
                                                                   ])
    def test_fan_list(self, client, to_user_id, action_type, num, size):
        user = Login(client, 'abcdf', '123456')
        user2 = Login(client, 'abcdef', '123456')
        response = client.post(
            '/relation/action',
            data={'to_user_id': to_user_id,
                  'action_type': action_type,
                  'page_num': num,
                  'page_size': size
                  },
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']}
        )

        response = client.get(
            '/follower/list',
            query_string={'user_id': user2.data['id']},
            headers={'Access-Token': user2.data['tokens']['access_token'],
                     'Refresh-Token': user2.data['tokens']['refresh_token']}
        )

        assert response.status_code == 200
        assert response.json['base']['code'] == 200
        fan_ids = [item['id'] for item in response.json['data']['items']]
        if action_type:
            assert user.data['id'] not in fan_ids
        else:
            assert user.data['id'] in fan_ids
