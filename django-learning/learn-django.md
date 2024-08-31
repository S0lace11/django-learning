# 环境配置

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

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set (defined as "choice_set") to hold the "other side" of a ForeignKey
# relation (e.g. a question's choice) which can be accessed via the API.
>>> q = Question.objects.get(pk=1)

# Display any choices from the related object set -- none so far.
>>> q.choice_set.all()
<QuerySet []>

# Create three choices.
>>> q.choice_set.create(choice_text="Not much", votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text="The sky", votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)

# Choice objects have API access to their related Question objects.
>>> c.question
<Question: What's up?>

# And vice versa: Question objects get access to Choice objects.
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

# Let's delete one of the choices. Use delete() for that.
>>> c = q.choice_set.filter(choice_text__startswith="Just hacking")
>>> c.delete(
```

