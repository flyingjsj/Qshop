from django.db import models

# Create your models here.
GENDER_STATUS = (
    (0, '女'),
    (1, '男')
)
TYPE_STATUS = (
    (0, '卖家'),
    (1, '买家'),
)
GoodsTYPE_STATUS = (
    (0, '上线'),
    (1, '下架'),
)


class User(models.Model):
    email = models.EmailField(default="sun@126.com")
    pwd = models.CharField(max_length=32)
    username = models.CharField(max_length=32, default="")
    phonenum = models.CharField(max_length=11, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(default=1, choices=TYPE_STATUS)
    gender = models.IntegerField(default=0, choices=GENDER_STATUS)
    photo = models.ImageField(upload_to="img", default="img/1.jpg")
    adress = models.TextField(default="石家庄")

    class Meta:
        db_table = "user"


class Goods_type(models.Model):
    type_name = models.CharField(max_length=32)
    pic = models.ImageField(upload_to="img", max_length=200)

    class Meta:
        db_table = "goods_type"


class Goods(models.Model):
    goods_number = models.CharField(max_length=11, verbose_name="商品编号")
    goods_name = models.CharField(max_length=11, verbose_name="商品名字")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_num = models.IntegerField(verbose_name="商品数量")
    type = models.IntegerField(default=0, choices=GENDER_STATUS)
    goods_pic = models.ImageField(upload_to="img", max_length=200, default="img/01.jpg")
    goods_type = models.ForeignKey(to=Goods_type, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = "goods"
