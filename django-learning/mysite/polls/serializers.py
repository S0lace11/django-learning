from rest_framework.serializers import *
from .models import *

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']