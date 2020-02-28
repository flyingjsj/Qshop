from django.shortcuts import render
from Seller.models import *
from .models import *
from django.http.response import HttpResponse, HttpResponseRedirect
import hashlib


# Create your views here.
def valid(func):
    def inner(request):
        username = request.COOKIES.get("b_username")
        s_username = request.session.get("b_username")
        if username and s_username and username == s_username:
            return func(request)
        else:
            return HttpResponseRedirect("/login")

    return inner


def setpwd(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result


def get_order_no():
    import uuid
    order_no = str(uuid.uuid4())
    return order_no

@valid
def index(request):
    res = []
    goods_types = Goods_type.objects.all()
    for type in goods_types:
        goods = Goods.objects.filter(goods_type_id=type.id)[:4]
        if goods:
            res.append({"type": type, "goods": goods})
    return render(request, "Buyer/index.html", locals())


def goods_list(request):
    flag = request.GET.get("flag")
    if flag == "l":
        typeid = request.GET.get("typeid")
        goods = Goods.objects.filter(goods_type_id=typeid)
    else:
        key = request.GET.get("key")
        goods = Goods.objects.filter(goods_name__icontains=key)
    newgoods = Goods.objects.order_by("-id")[:3]
    return render(request, "Buyer/list.html", locals())


def detail(request):
    id = request.GET.get("id")
    goods = Goods.objects.filter(id=id).first()
    newgoods = Goods.objects.order_by("-id")[:2]
    return render(request, "Buyer/detail.html", locals())

@valid
def cart(request):
    user_id = request.COOKIES.get("b_user_id")
    goods_id = request.GET.get("goods_id")
    goods_count = int(request.GET.get("goods_count"))
    ## 查找商品
    goods = Goods.objects.get(id=goods_id)
    payOrder = PayOrder.objects.filter(order_status=0).first()
    if payOrder:
        pass
    else:
        payOrder = PayOrder()
        payOrder.order_number = get_order_no()
        payOrder.order_status = 0  ### 未生成状态
        payOrder.order_total = goods_count * goods.goods_price
        payOrder.order_user_id = int(user_id)
        payOrder.save()
    ##生成订单详情
    order_info = OrderInfo()
    order_info.order = payOrder
    order_info.goods = goods
    order_info.goods_price = goods.goods_price
    order_info.order_status = 0
    ## 店铺的信息 通过商品寻找 店铺
    order_info.store = goods.user
    order_info.goods_count = goods_count
    order_info.goods_total_price = goods_count * goods.goods_price
    order_info.save()

    orders = OrderInfo.objects.filter(order_status=0)

    return render(request, "Buyer/cart.html", locals())


def place_order(request):
    pid = request.GET.get("pid")
    payorder = PayOrder.objects.filter(id=pid).first()
    payorder.order_status = 1
    count = 0
    total = 0
    for order in payorder.orderinfo_set.all():
        order.order_status = 1
        count += order.goods_count
        total += order.goods_total_price
    totals = total+10
    totals = round(totals, 2)
    return render(request, "Buyer/place_order.html", locals())


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        user = User.objects.filter(username=username, pwd=setpwd(pwd), type=1).first()
        if user:
            result = HttpResponseRedirect("/")
            result.set_cookie("b_username", username)
            result.set_cookie("b_user_id", user.id)
            request.session["b_username"] = username
            return result
        else:
            msg = "用户名密码错误"
    else:
        return render(request, "Buyer/login.html")


def register(request):
    if request.method == "POST":
        user = User()
        user.username = request.POST.get("user_name")
        user.pwd = setpwd(request.POST.get("pwd"))
        user.save()
        return HttpResponseRedirect("/login/")
    else:
        return render(request, "Buyer/register.html")


def logout(request):
    result = HttpResponseRedirect("/login/")
    result.delete_cookie("b_username")
    del request.session["b_username"]
    return result
