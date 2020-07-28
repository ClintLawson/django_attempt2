from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_login_register),
    path('register', views.register),
    path('login', views.login),
    path('edit_account/', views.edit_account),
    path('logout/', views.logout),
    path('update_account/', views.update_account), 

]