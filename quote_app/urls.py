from django.urls import path
from . import views

urlpatterns = [
    path('quotes/', views.view_all_quotes),
    path('add_quote/', views.add_quote), 
    path('like_quote/<quote_id>', views.like_quote),
    path('user/<user_id>', views.view_user),
    path('delete_quote/<quote_id>', views.delete_quote)
]