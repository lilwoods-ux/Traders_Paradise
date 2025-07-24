from django.urls import path
from . import views

urlpatterns = [
    path('', views.bot_list, name='bot_list'),
    path('api/mpesa/stk-push/', views.stk_push, name='stk_push'),
    path('signup/', views.user_signup, name='signup'),
    path('upload/', views.upload_bot, name='upload_bot'),
    path('delete/<int:bot_id>/', views.delete_bot, name='delete_bot'),
    path('homepage/', views.homepage, name='homepage'),  # Ensure homepage is here
    path('payment/<int:bot_id>/', views.payment, name='payment'),  # Payment page
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('payment/success/<int:bot_id>/', views.payment_success, name='payment_success'),
]