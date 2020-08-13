from django.urls import path

from . import views

urlpatterns = [
    path('ids_and_input_data/', views.ids_and_input_data, name='ids_and_input_data'),
    path('invalid_id/', views.invalid_id, name='invalid_id'),
    path('<id>/', views.categories, name='categories'),
    path('<id>/<cat>/', views.book_category, name='book_category'),
    path('<title>/', views.detail, name='detail'),
]