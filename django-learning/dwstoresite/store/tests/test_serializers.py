from django.test import TestCase

from store.models import *
from store.serializers import *

class StudentsSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        classroom = Classroom.objects.create(name='一班', grade=4)
        Student.objects.create(name='小兰', age=14, classroom=classroom)

    def test_students_serialization(self):
        student = Student.objects.get(age=14)
        serializer = StudentSerializer(student)
        data = serializer.data
        self.assertEqual(data['name'], '小兰')