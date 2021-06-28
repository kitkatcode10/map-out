from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('vacations/', views.vacations_index, name='index'),
    path('vacations/<int:vacation_id>/', views.vacations_detail, name='detail'),
]