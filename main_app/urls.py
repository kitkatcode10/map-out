from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('vacations/create/', views.VacationCreate.as_view(), name='vacations_create'), 
    path('vacations/<int:pk>/update/', views.VacationUpdate.as_view(), name='vacations_update'),
]

