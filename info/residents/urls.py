from django.urls import path

from .views import ResidentDetailView, HouseListView, HouseDetailView, ResidentCreateView

urlpatterns = [
    path('house/', HouseListView.as_view(), name='houses-list'),
    path('house/<int:pk>/', HouseDetailView.as_view(), name='houses-detail'),
    path('house/<int:house_id>/residents/<int:pk>/', ResidentDetailView.as_view(), name='resident-detail'),
    path('house/<int:house_id>/residents/new/', ResidentCreateView.as_view(), name='resident-create'),
]

