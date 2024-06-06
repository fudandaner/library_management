from django.db import models


# Create your models here.
class Books(models.Model):
    BookID = models.AutoField(primary_key=True)
    Title = models.CharField(verbose_name="书名", max_length=64)
    Author = models.CharField(verbose_name="作者", max_length=64)
    Publisher = models.CharField(verbose_name="出版社", max_length=64)
    PublishDate = models.DateField(verbose_name="出版日期")
    Price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    ISBN = models.CharField(verbose_name="书号", max_length=64)
    StockQty = models.IntegerField(verbose_name="图书存量", default=1)
    lend_choices = (
        (1, "未借出"),
        (2, "已借出"),
    )
    LendState = models.SmallIntegerField(verbose_name='借阅状态', choices=lend_choices, default=1)


class Students(models.Model):
    StudentID = models.AutoField(primary_key=True)
    Password = models.CharField(verbose_name="密码", max_length=64,null=True, blank=True)
    Name = models.CharField(verbose_name="姓名", max_length=64)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    Gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    Grade = models.IntegerField(verbose_name="年级")
    Major = models.CharField(verbose_name="专业", max_length=64)


class BorrowRecords(models.Model):
    BorrowID = models.AutoField(primary_key=True)
    BorrowDate = models.DateField(verbose_name="借阅日期")
    ReturnDate = models.DateField(verbose_name="归还日期", null=True, blank=True)
    BookID = models.ForeignKey(to='Books', to_field='BookID', on_delete=models.CASCADE)
    StudentID = models.ForeignKey(to='Students', to_field='StudentID', on_delete=models.CASCADE)
