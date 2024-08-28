from werkzeug.datastructures import FileStorage
from app.config import IMAGE_PATH
from .conftest import Login


class TestAvatar(object):
    # 正常上传头像
    def test_upload(self, client):
        user = Login(client, 'abcdf', '123456')
        file = FileStorage(stream=open(IMAGE_PATH + '1.jpg', 'rb'), filename='1.jpg')
        response = client.post(
            '/user/avatar/upload',
            data={'data': file},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']},
        )
        # print(response.json['base']['msg'])
        assert response.status_code == 200

    # 文件格式错误
    def test_upload_wrong_file(self, client):
        user = Login(client, 'abcdf', '123456')
        file = FileStorage(stream=open('./test.txt', 'rb'),
                           filename='test_avatar/test.txt')
        response = client.post(
            '/user/avatar/upload',
            data={'data': file},
            headers={'Access-Token': user.data['tokens']['access_token'],
                     'Refresh-Token': user.data['tokens']['refresh_token']},
        )
        assert response.status_code == 422

    # 正常获取图片
    def test_avatar(self, client):
        user = Login(client, 'abcdf', '123456')
        # print(user.data['avatar_url'])
        response = client.get('/user/avatar/' + user.data['avatar_url'].split('/')[-1])
        assert response.status_code == 200
