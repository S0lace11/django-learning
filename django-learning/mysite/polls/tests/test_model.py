import datetime

from django.test import TestCase
from django.utils import timezone

from ..models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'question_text': 'test',
            'pub_date': timezone.now()  # 使用当前时间作为发布日期
        }
        Question.objects.create(**kwargs)

    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIsNotNone(future_question.was_published_recently(),False)
        