from django.urls import path

from . import views

urlpatterns = [
    path('', views.categories, name='categories'),
    path('<cat>/', views.book_category, name='book_category'),
    path('<cat>/<title>/', views.detail, name='detail'),
]