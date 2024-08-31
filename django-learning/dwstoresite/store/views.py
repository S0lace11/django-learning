from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Classroom, Student
from .serializers import ClassroomSerializer, StudentSerializer
# Create your views here.


# class ClassroomListView(APIView):
#     def get(self, request):
#         classrooms = Classroom.objects.all()
#         serializer = ClassroomSerializer(classrooms, many=True)
#         return Response(serializer.data)

# class StudentListView(APIView):
#     def get(self, request):
#         students = Student.objects.all()
#         serializer = StudentSerializer(students, many=True)
#         return Response(serializer.data)
    
class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer