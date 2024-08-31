from django.db import models

# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    grade = models.IntegerField()

    def __str__(self):
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return self.name