from django.urls import path
from rest_framework.routers import DefaultRouter
from store.views import *

urlpatterns = [
    # path('classrooms/', ClassroomListView.as_view(), name='classroom-list'),
    # path('students/', StudentListView.as_view(), name='student-list'),
]

router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet)
router.register(r'students', StudentViewSet)

urlpatterns += router.urls