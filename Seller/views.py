import hashlib

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, QueryDict
from django.views.generic import View
from .models import *


# Create your views here.

# Create your views here.
def valid(func):
    def inner(request):
        email = request.COOKIES.get("email")
        s_email = request.session.get("email")
        if email and s_email and email == s_email:
            return func(request)
        else:
            return HttpResponseRedirect("/Seller/login")

    return inner


def setpwd(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result


def register(request):
    msg = ""
    if request.method == "POST":
        email = request.POST.get("email")
        pwd = request.POST.get("password")
        repwd = request.POST.get("repassword")
        if email and pwd and pwd == repwd:
            if User.objects.filter(email=email).exists():
                msg = "用户名已存在"
            else:
                User.objects.create(email=email, pwd=setpwd(pwd), type=0)
                return HttpResponseRedirect("/Seller/login")
        else:
            msg = "参数为空"

    return render(request, "Seller/register.html", locals())


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        pwd = request.POST.get("password")
        user = User.objects.filter(email=email, pwd=setpwd(pwd), type=0).first()
        if user:
            result = HttpResponseRedirect("/Seller/index")
            result.set_cookie("email", email)
            result.set_cookie("id", user.id)
            request.session["email"] = email
            return result
        else:
            msg = "用户名密码错误"
    return render(request, "Seller/login.html", locals())


def logout(request):
    result = HttpResponseRedirect("/Seller/login")
    result.delete_cookie("email")
    del request.session["email"]
    return result


@valid
def index(request):
    return render(request, "Seller/index.html")


def me(request):
    id = request.COOKIES.get("id")
    user = User.objects.filter(id=id).first()
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phonenum = request.POST.get("phonenum")
        user.age = request.POST.get("age")
        user.gender = int(request.POST.get("gender"))
        user.adress = request.POST.get("adress")
        if request.FILES.get("image"):
            user.photo = request.FILES.get("image")
        user.save()
        # return HttpResponseRedirect("/Seller/me")

    return render(request, "Seller/me.html", locals())


def goods(request):
    type = request.GET.get("type")
    mygoods = Goods.objects.filter(type=type)

    return render(request, "Seller/goods.html", locals())


class goodscreate(View):
    def get(self, request):
        goods_type = Goods_type.objects.all()
        return render(self.request, "Seller/goodscreate.html", locals())

    def post(self, request):
        my_goods = Goods()
        my_goods.goods_number = self.request.POST.get("goods_number")
        my_goods.goods_name = self.request.POST.get("goods_name")
        my_goods.goods_price = self.request.POST.get("goods_price")
        my_goods.goods_num = self.request.POST.get("goods_num")
        my_goods.type = self.request.POST.get("type")
        my_goods.goods_type_id = self.request.POST.get("goods_type")
        id = request.COOKIES.get("id")
        my_goods.user = User.objects.filter(id=id).first()
        if request.FILES.get("pic"):
            my_goods.goods_pic = request.FILES.get("pic")
        my_goods.save()
        return JsonResponse({'state': 200, 'msg': "新增成功"})

    def delete(self, request):
        rdel = QueryDict(request.body, encoding=request.encoding)
        id = rdel.get('id')
        de_goods = Goods.objects.filter(id=id).first()
        de_goods.type = 1
        de_goods.save()
        return JsonResponse({'state': 200, 'msg': "下架成功"})
