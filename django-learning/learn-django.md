# 环境配置

安装 anaconda, vscode

```shell
pip install django # 安装 django
```

# 创建 Django 项目和 APP
## 创建项目

进入你需要创建项目的目录

```shell
django-admin startproject mysite #最后一个参数填写你自己的项目名称
```

项目结构图

![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240830131249584.png)

`manage.py` 提供了一种命令行工具，方便你与你的 Django 项目互动

`urls.py` Django 项目的 URL 设置，你的 Django 网站目录

**重要**：`settings.py ` 包含项目的配置文件

```python
# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("polls/", include("polls.urls")), # 将应用内的urls封装在include中，方便管理
    path('admin/', admin.site.urls), # 管理员路径
]
```



## 创建应用

```shell
python manage.py startapp polls # 最后一个参数是你的 app 名称
```

项目结构图

![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240830132131375.png)

`models.py` 文件与数据库相关，用 python 来描述数据表

`admin.py` 与后台管理相关

`views.py` 页面业务逻辑，接受请求，处理

# 配置 `settings.py` 和启动项目
## settings.py

**INSTALLED_APPS**：这个列表包含了所有已安装的Django应用，包括Django内置的应用和你自己创建的应用。每个应用都可以提供不同的功能，如用户认证、管理界面等，官方文档加入的参数是 `"polls.apps.PollsConfig",`

**DATABASES**：这个设置定义了数据库的配置，包括数据库引擎、名称、用户、密码等。Django支持多种数据库，如SQLite、PostgreSQL、MySQL等。

**LANGUAGE_CODE** 和 **TIME_ZONE**：这些设置定义了项目的语言和时区。可以根据需要进行修改。

## 启动项目

运行项目先执行数据库相关操作

```shell
python manage.py makemigrations (polls) # 最后一个参数可以选择填入你应用名
python manage.py migrate
```

启动 Django 服务

```shell
python manage.py runserver
```

浏览器内打开对应链接 http://127.0.0.1:8000/

![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240830135314590.png)

# Django 数据库构建与数据迁移

## 数据库构建

在 `polls/models.py` 内创建类，构建字段

Question 类包含问题内容 `question_text` ，发布时间 `pub_date` 

Choice 类包含问题外键 `question`， 选项内容 `choice_text`，投票数量 `votes` 

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    # 这段代码在后续的测试案例中会报错，需要修改
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) # 判断是否发布在 24 小时之内
    
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # CASCADE表示与之关联的数据也被删除
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
```

## 合并数据库

运行项目先执行数据库相关操作

```shell
python manage.py makemigrations
```

这个命令用于生成迁移脚本，迁移脚本用于告诉数据库如何根据这些结构变化进行更新。当你更新了模型文件之后，需要运行该命令，Django 会检测模型的改变，然后自动生成相应的迁移脚本，存储在 `migrations/` 目录下。通常来说，你需要针对每个应用运行一次该命令。

```shell
python manage.py migrate
```

这个命令用于将迁移脚本应用到数据库中。当你在模型文件中进行更改之后，需要先通过 `makemigrations` 命令生成迁移脚本，然后运行该命令将这些脚本应用到数据库中。对于新的迁移脚本，Django 会逐个执行它们，从而更新数据库结构。对于已经执行过的脚本，Django 会跳过它们，避免重复执行。

## 数据库常用字段与配置

`CharField` 用于存储字符串类型，有最大长度限制

`IntegerField` 用于存储整数类型

`FloatField`用于存储浮点数类型

`BooleanField` 用于存储布尔类型

`DateField` 用于存储日期类型

`DateTimeField` 用于存储日期和时间类型

`ImageField` 用于存储图片类型

`FileField` 用于存储文件类型

`ForeignKey` **外键** 用于表示数据库表之间的关联关系

`OneToOneField` **一对一** 用于表示数据库表之间的一对一关系

`ManyToManyField` **多对多** 用于表示数据库表之间多对多的关联关系 

# 引入 Django 后台和管理员用户

## 创建管理员用户

```shell
python manage.py runuser
```

根据指引分别输入用户名，邮箱，密码（8位密码不能是纯数字）

登录 admin 后台

http://127.0.0.1:8000/admin

## 配置

在 `admin.py` 注册

```python
from django.contrib import admin
from .models import Question # 引入 Question

# Register your models here.

admin.site.register(Question)
```

# 数据库操作测试

可以选择进入 python 终端进行数据库的增删改查

```shell
python manage.py shell
```

通过命令行进行数据的增删改查

`QuerySet []` 是从数据库查询出来的一个集合

```shell
>>> from polls.models import Question, Choice # 导入类

# 系统内还没问题
>>> Question.objects.all()
<QuerySet []>

>>> from django.utils import timezone # 导入 timezone 类
>>> q = Question(question_text="What's new?", pub_date=timezone.now()) # 创建一个问题，发布时间为现在

>>> q.save() # 保存该问题

>>> q.id # 查看问题 id
1

>>> q.question_text # 查看问题内容
"What's new?"

>>> q.pub_date # 查看问题发布时间
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=datetime.timezone.utc)

>>> q.question_text = "What's up?" # 更改问题内容
>>> q.save() # 保存该问题

>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```

对 Choice 类增删改查

```shell
>>> from polls.models import Choice, Question# 导入类

>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>

>>> Question.objects.filter(id=1) # 查找 id=1 的问题
<QuerySet [<Question: What's up?>]>

>>> Question.objects.filter(question_text__startswith="What") # 查找以 'what' 开头的问题
<QuerySet [<Question: What's up?>]>

>>> from django.utils import timezone
>>> current_year = timezone.now().year # 获取当前年份
>>> Question.objects.get(pub_date__year=current_year) # 查询今年发布的问题
<Question: What's up?>

>>> Question.objects.get(id=2) # 查找 id=2 的问题，因为不存在所以报错
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

>>> Question.objects.get(pk=1) # 查询主键值为 1 的问题，因为 id 为主键，相当于查询 id=1 的问题
<Question: What's up?>

>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently() # 是否最近发布
True

>>> q = Question.objects.get(pk=1)

>>> q.choice_set.all() # 查询当前问题(q)的所有选择(choice)，返回的是一个集合
<QuerySet []>

# 创建 3 个选择(choice)
>>> q.choice_set.create(choice_text="Not much", votes=0)
<Choice: Not much>

>>> q.choice_set.create(choice_text="The sky", votes=0)
<Choice: The sky>

>>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)

# choice 同样可以查询对应的问题(question)
>>> c.question
<Question: What's up?>

>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count() # 查询当前问题(q)所有选择(choice)的数量()
3

>>> Choice.objects.filter(question__pub_date__year=current_year) # 查询今年发布的选择(choice)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

>>> c = q.choice_set.filter(choice_text__startswith="Just hacking")
>>> c.delete() # 删除筛选的数据
```

# Django APIView 与 Serialization

## APIView

> APIView 是 Django REST Framework 提供的一个视图类。它和 Django 中的 view 类有些相似，但是又有一些不同之处。APIview 可以处理基于 HTTP 协议的请求，并返回基于内容协商的响应，它旨在提供一个易于使用且灵活的方式来构建 API 视图。

```python
# polls/views.py
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *

class GetQuestions(APIView):
    def get(self,request):
        questions = Question.objects.all() # 获取所有的Question实例
        serializer = QuestionSerializer(instance=questions, many=True) # 对获取的所有的questions进行实例化
        print(serializer.data)
        return Response(serializer.data) # 返回所有序列化后的实例
    
    def post(self,request):
        # 从请求数据中提取字段
        request_data = {
            "question_text": request.data.get("question_text")
            "pub_date":timezone.now()
        }

        new_question = Question.objects.create(**request_data) # 引用request_data中的数据创建一个新的实例

        serializer = QuestionSerializer(instance=new_question) # 对新的实例进行实例化
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
```

还需要在 `urls.py` 文件中注册这些方法，使之可以被 GET/POST

```##python
# polls/urls.py
from django.urls import path

from .views import GetQuestions,FilterQuestionsAPI

from .models import Question

urlpatterns = [
	...
    path("getquestions/", GetQuestions.as_view()),
    path("filterquestionsapi/", FilterQuestionsAPI.as_view())
]
```

## 序列化 Serializer

> **序列化**是将复杂的Python数据结构（如Django模型实例或者查询集）转换成易于存储或传输的格式，如JSON、XML等。这个过程对于构建API至关重要，因为Web应用通常需要以JSON格式交换数据。序列化器定义了数据的结构和转化规则，确保输出的数据格式正确且安全。

```python
# polls/serializers.py
from rest_framework.serializers import *
from .models import *

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
```

## Postman

Postman 是一款流行的

GET

![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240902203210059.png)

POST

# 单元测试

应用下有一个 `tests.py` 文件，负责测试各个单元程序运行是否正常，运行测试前自动生成数据，测试完成后自动删除数据，不影响数据库内容。

输入以下命令进行测试

```shell
python manage.py test 你的应用名
```



![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240831161741433.png)

为了方便进行多个测试，保证代码简洁，可以选择删除 `tests.py` 在同一目录下创建 tests 包，在 tests 文件夹下新建一个空的 `init.py` 文件构成包，并逐一添加测试程序

> **注意** tests 包中的各个模块必须以 test_ 开头，否则 django 无法发现这些测试文件的存在，从而不会运行里面的测试用例。

django 应用的单元测试包括：

- 测试 model，model 的方法是否返回了预期的数据，对数据库的操作是否正确。
- 测试序列化器
- 测试视图，针对特定类型的请求，是否返回了预期的响应
- 其它的一些辅助方法或者类等

## model 测试

在 tests 包下创建  `test_model.py` 文件

官方给出的案例中，创建一个 30 天后的问题实例，在判断是否最近发布时为 True，显然错误

![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240902160605005.png)

创建测试类

```python
# polls/tests/test_model.py
import datetime

from django.test import TestCase # 导入测试类
from django.utils import timezone # 导入时区类

from ..models import Question # 导入Question类

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False) # 检查该方法的返回值，应该是False
```

**测试**

命令行中输入下面的指令
```shell
python manage.py test polls
```

![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240902162849418.png)

发现报错了，说明我们的 `was_publised_recentlly` 方法设计有错误

我们重新设计该方法，如果 `pub_date` 在昨天和今天之间，返回 True

```python
# polls/models.py
...
class Question(models.Model):
...
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
...
```

重新进行测试，这样就是运行成功

![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240902163957409.png)

## 测试序列化器

在 tests 包下创建  `test_serializer.py` 文件

`QuestionSerializerTest`  类用于测试 QuestionSerializer 序列化器

`setUpTestData` 创建测试数据，方便后续序列化测试

`test_question_serialization` 验证能否序列化

这里的案例举得不是特别恰当，如果最后结果匹配则测试成功

```python
# polls/tests/test_serialziers.py
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

```

![](C:\Users\13630\AppData\Roaming\Typora\typora-user-images\image-20240902190301411.png)



## 测试视图

在 tests 包下创建  `test_views.py` 文件

该测试文件主要用来测试视图工作，测试视图通过模拟HTTP请求并检查视图的响应来确保视图逻辑的正确性。这有助于开发者在修改或添加新功能时，确保现有功能不受影响，提高应用的稳定性和可靠性。

**Client 工具**

Client 用来模拟用户和视图层代码的交互

```python
from django.test.utils import setup_test_environment 
setup_test_environment() # 模板渲染器，下面的内容会针对现有的数据库运行
from django.test import Client
# 创建一个供用户使用的 client 实例
client = Client()
```



### 测试新视图

创建了一个 `QuestionIndexViewTests` 测试类，分别创建不同的组合来模拟视图可能出现的情况

```python
# polls/tests/test_views.py
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
        获取最新问题列表应为发布在过去的 Question 实例
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question], 
        )

    def test_future_question(self):
        """
        获取最新问题列表应该为空，创建的 Question 实例在未来
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        获取最新问题列表应该为发布在过去的 Question 实例，未来的 Question 实例不会出现
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
        获取最新问题列表为发布在过去的 Question 实例，如果有多个，则都会显示
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
```

### 测试 DetailView

用户只能在 URL 中访问过去的实例，我们需要在 DetailView 增加约束

```python
# polls/views.py
class DetailView(generic.DetailView):
    ...

    def get_queryset(self):
        """
        排除不是最近发布的问题
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
```



测试发布在未来的 Question 实例不会被访问到，用户只能访问过去的 Question 实例

```python
# polls/tests/test_views.py
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
```



