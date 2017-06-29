from django.test import TestCase
from .models import User


# Create your tests here

def CreatUser(user_id1,user_id2,user_id3):
    User.objects.create(user_id=user_id1, user_name='111', pwd='123', user_type='1')
    User.objects.create(user_id=user_id2, user_name='222', pwd='123', user_type='1')
    User.objects.create(user_id=user_id3, user_name='333', pwd='123', user_type='1')


class SQLtest(TestCase):
    def test_raw(self):
        CreatUser(1,2,3)
        for u in User.objects.raw('Select * from sqltrainapp_user'):
            # 查询的字段中必须包含主键，且查询的结果都是实例。
            print(u)
        for x in User.objects.raw('Select user_id,max(user_id) from sqltrainapp_user'):
            print(x.user_id)
        print(int(User.objects.raw('Select user_id,max(user_id) from sqltrainapp_user')[0].user_id)+1)
        # for x in User.objects.raw('Select max(user_id) from sqltrainapp_user'):
        #     print(x.user_id)
        print(User.objects.raw('Select *,max(user_id) from sqltrainapp_user'))
        # print(User.objects.raw('Select user_id from sqltrainapp_user'))
