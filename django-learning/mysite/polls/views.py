from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404,render
from django.db.models import F
from django.views import generic
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .serializers import *

from .models import Question, Choice


# Create your views here.



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5] # 返回最新的前5个Question实例，-pub_date 降序排列
        # 筛选发布日期小于或等于现在时间的Question实例 lte=less than or equal to
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


# API 测试
class GetQuestions(APIView):
    def get(self,request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(instance=questions, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
    def post(self,request):
        # 从请求数据中提取字段
        request_data = {
            "question_text": request.data.get("question_text"),
            "pub_date":timezone.now()
        }

        new_question = Question.objects.create(**request_data)

        serializer = QuestionSerializer(instance=new_question)
        return Response(serializer.data)
    
class FilterQuestionsAPI(APIView):

    def get(self, request, format=None):
        print(request.method)
        return Response('ok')

    def post(self, request, format=None):
        print(request.method)
        return Response('ok')

    def put(self, request, format=None):
        print(request.method)
        return Response('ok')
    