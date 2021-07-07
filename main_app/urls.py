from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('vacations/', views.vacations_index, name='index'),
    path('vacations/<int:vacation_id>/', views.vacations_detail, name='detail'),
    path('vacations/create/', views.VacationCreate.as_view(), name='vacations_create'), 
    path('vacations/<int:pk>/update/', views.VacationUpdate.as_view(), name='vacations_update'),
    path('vacations/<int:pk>/delete/', views.VacationDelete.as_view(), name='vacations_delete'),
    path('vacations/<int:vacation_id>/add_itinerary/', views.add_itinerary, name='add_itinerary'),
    path('vacations/<int:vacation_id>/delete_itinerary/<int:itinerary_id>', views.delete_itinerary, name='delete_itinerary'),
    path('vacations/<int:vacation_id>/assoc_packing/<int:packing_id>/', views.assoc_packing, name='assoc_packing'), 
    path('vacations/<int:vacation_id>/unassoc_packing/<int:packing_id>/', views.unassoc_packing, name='unassoc_packing'),
    path('vacations/<int:vacation_id>/add_photo/', views.add_photo, name='add_photo'),
    path('packing/', views.PackingList.as_view(), name='packing_index'),
    path('packing/<int:pk>/', views.PackingDetail.as_view(), name='packing_detail'),
    path('packing/create/', views.PackingCreate.as_view(), name='packing_create'),
    path('packing/<int:pk>/update/', views.PackingUpdate.as_view(), name='packing_update'),
    path('accounts/signup/', views.signup, name='signup'), 
]

