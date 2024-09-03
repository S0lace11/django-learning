from django.test import TestCase
from ..serializers import QuestionSerializer
from ..models import Question

class QuestionSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'question_text': 'test',
            'pub_date': '2024-09-02 8:00:00'
        }
        Question.objects.create(**kwargs)

    def test_question_serialization(self):
        question = Question.objects.get(pub_date='2024-09-02 8:00:00')
        serializer = QuestionSerializer(question)
        data = serializer.data
        self.assertEqual(data['question_text'], 'test')

