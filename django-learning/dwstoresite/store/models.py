from django.db import models

# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=100, verbose_name='班级名')
    grade = models.IntegerField(verbose_name='年级')

    def __str__(self):
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return self.name