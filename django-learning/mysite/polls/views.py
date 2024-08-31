from django.http import HttpResponse,Http404
from django.template import loader
from django.shortcuts import get_object_or_404,render
from .models import Question

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import *

# Create your views here.
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


# @api_view(["GET","POST"])
# def InsertQuestion(request):
#     q_text = request.data.get('问题')

#     # 获取分类对象或创建新的分类对象
#     question, created = Question.objects.get_or_create(question_text=q_text)

#     # 判断是否已存在分类
#     if not created:
#         return Response({"status":"已存在", "question":q_text},status=200)
#     else :
#         return Response({"message":f"Successfully inserted question'{q_text}'."})
    
# @api_view(["GET","POST"])
# def FilterQuestion(request):
#     data = request.data.get('问题')
#     questions = Question.objects.filter(name=data)
#     if questions.exists():
#         return Response({"status":"已存在", "question":data},status=200)
#     else:
#         return Response({"status":"不存在", "question":data},status=404)

class GetQuestions(APIView):
    def get(self,request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(instance=questions, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
    def post(self,request):
        # 从请求数据中提取字段
        request_data = {
            "question": request.data.get("q_text")
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
    