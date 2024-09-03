import datetime
from django.urls import reverse
from django.test import TestCase
from ..models import Question
from django.utils import timezone

# 设计一个创建question实例方法，方便代码复用
def create_question(question_text, days):

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        # self.client 向应用的 'index' 视图发送一个 GET 请求，reverse("polls:index") 根据 URL 的命名动态生成实际的 URL
        self.assertEqual(response.status_code, 200)
        # 请求成功且服务器返回了预期的内容
        self.assertContains(response, "No polls are available.")
        # 如果没有投票可用，返回该消息
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        # 没有投票存在的情况下，试图获取的最新问题列表为空

    def test_past_question(self):
        """
        获取最新问题列表应为发布在过去的 question 实例
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question], 
        )

    def test_future_question(self):
        """
        获取最新问题列表应该为空，创建的 question 实例在未来
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        获取最新问题列表应该为发布在过去的 question 实例，未来的 question 实例不会出现
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        获取最新问题列表为发布在过去的 question 实例，如果有多个，则都会显示
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        发生在将来的问题不会出现在列表中，返回 404
        """
        future_question = create_question(question_text='future_question', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        发生在过去的问题会显示文本中
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)