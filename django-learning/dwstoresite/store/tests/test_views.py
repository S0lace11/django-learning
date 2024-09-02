from store.models import *
from rest_framework.test import APITestCase
from rest_framework import status

class ClassroomsViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Classroom.objects.create(name='二班', grade=4)

    def test_get_classroom(self):
        response = self.client.get('/classrooms/')
        print(response.status_code)  # 打印状态码
        print(response.data)          # 打印返回的数据
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class GetClassroomsTest(APITestCase):
    def test_get_classroom(self):
        response = self.client.get('getclassrooms')
        self.assertEqual(response.status_code, status.HTTP_200_OK)