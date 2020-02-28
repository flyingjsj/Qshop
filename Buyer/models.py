from django.db import models
from Seller.models import User, Goods

# Create your models here.

ORDER_STATUS = (
    (0, "未生成"),
    (1, "未支付"),
    (2, "已支付"),
    (3, "待发货"),
    (4, "已发货"),
    (5, "拒收"),
    (6, "已完成"),
)
ORDERINFO_STATUS = (
    (0, "未生成"),
    (1, "已生成"),
)


class PayOrder(models.Model):
    order_number = models.CharField(max_length=64, unique=True, verbose_name="订单号")
    order_date = models.DateField(auto_now=True, verbose_name="订单创建时间")
    order_status = models.IntegerField(choices=ORDER_STATUS, verbose_name="订单状态")
    order_total = models.FloatField(verbose_name="订单总价")
    order_user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="买家")

    class Meta:
        db_table = "pay_order"


class OrderInfo(models.Model):
    order = models.ForeignKey(to=PayOrder, on_delete=models.CASCADE)
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE)
    goods_price = models.FloatField(verbose_name="商品的单价")
    store = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="卖家")
    goods_count = models.IntegerField(verbose_name="购买的单品的数量")
    goods_total_price = models.FloatField(verbose_name="购买的单品的总金额")
    order_status = models.IntegerField(choices=ORDERINFO_STATUS,verbose_name="订单状态")

    class Meta:
        db_table = "order_info"
