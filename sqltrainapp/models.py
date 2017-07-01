from django.db import models
# Create your models here.

# 用户：用户名、密码、用户类型（编号or名称）、学校(编号or名称)、专业（编号or名称）、班级（编号or名称）
# 安照国家的编号，学校编号长度5位。专业分12大类，长度最长6位。
# primary_key 指定主键
# Meta 指定表名称
class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)

    user_name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    user_type = models.CharField(max_length=2)

    school = models.CharField(max_length=5)
    faculties = models.CharField(max_length=6)
    cls = models.CharField(max_length=2)

    def __str__(self):
        return self.user_name
    # class Meta:
    #   db_table="users"

# 题目：类型(标示12个专业不同课程的内容)、标题、内容、参考答案、难度等级、通过人数、做这道题的总人数
class Question(models.Model):
    ques_id = models.AutoField( primary_key=True,  verbose_name='ID') # 使用django默认的id也可以

    submit_user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)

    ques_type = models.CharField(max_length=10)
    ques_title = models.CharField(max_length=200)
    ques_content = models.CharField(max_length=800)
    answer = models.CharField(max_length=700)
    level = models.CharField(max_length=2)

    passnum = models.IntegerField(default=0)
    totalnum = models.IntegerField(default=0)

    def __str__(self):
        return self.ques_title

# 做题：某人、某题、开始答题时间（写答案开始）、结束答题时间（提交）、答题内容、占用内存、使用语言、运行结果（类型or内容）
# 	int : 2 147 483 647
class Doques(models.Model):
    run_id = models.AutoField(primary_key=True, unique=True)

    someone = models.ForeignKey(User, on_delete=models.CASCADE)
    someques = models.ForeignKey(Question, on_delete=models.CASCADE)

    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    answ_content = models.CharField(max_length=1000)
    memory = models.CharField(max_length=10)
    language_type = models.CharField(max_length=2)
    result_type = models.CharField(max_length=2)

    def __str__(self):
        return str(self.run_id)







