from django.urls import path, include
from .views import *

urlpatterns = [
    path('index/', index),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('me/', me),
    path('goods/', goods),
    path('goodscreate/', goodscreate.as_view()),
]
