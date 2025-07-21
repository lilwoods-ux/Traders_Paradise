from django.urls import path
from . import views

urlpatterns = [
    path('', views.bot_list, name='bot_list'),  # '' now means /bots/
    path('api/mpesa/stk-push/', views.stk_push, name='stk_push'),
    path('signup/', views.signup, name='signup'),
    path('upload/', views.upload_bot, name='upload_bot'),
    path('delete/<int:bot_id>/', views.delete_bot, name='delete_bot'),
]