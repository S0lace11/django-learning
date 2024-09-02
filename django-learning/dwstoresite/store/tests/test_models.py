from django.test import TestCase
from store.models import *

class ClassroomTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Classroom.objects.create(name='一班',grade=3)

    def test_name_labels(self):
        classroom = Classroom.objects.get(id=1)
        field_label = classroom._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'班级名')


class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 设置测试数据
        classroom = Classroom.objects.create(name='一班',grade=3)
        Student.objects.create(name='张三', age=20, classroom=classroom)

    def test_name_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('name').verbose_name
        self.assertEqual(field_label, '姓名')  # 根据你的模型字段的verbose_name进行修改

    def test_age_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('age').verbose_name
        self.assertEqual(field_label, '年龄')  # 根据你的模型字段的verbose_name进行修改

    def test_name_max_length(self):
        student = Student.objects.get(id=1)
        max_length = student._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)  # 根据你的模型字段的max_length进行修改

    def test_age_value(self):
        student = Student.objects.get(id=1)
        self.assertEqual(student.age, 20)  # 验证年龄是否正确