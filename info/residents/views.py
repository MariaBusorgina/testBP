from rest_framework import generics

from .models import House, Resident
from .serializers import HouseSerializer, HouseDetailSerializer, ResidentDetailSerializer, ResidentCreateSerializer


class HouseListView(generics.ListAPIView):
    """Представление для отображения списка всех домов"""
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class HouseDetailView(generics.RetrieveAPIView):
    """Представление для отображения подробной информации о выбранном доме, включая список всех жильцов"""
    queryset = House.objects.all()
    serializer_class = HouseDetailSerializer

    def get_object(self):
        house = super().get_object()
        house.residents = Resident.objects.filter(ownerships__apartment__house=house).distinct().order_by('full_name')
        return house


class ResidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Представление для просмотра, обновления информации о конкретном жильце, удаление жильца"""
    serializer_class = ResidentDetailSerializer

    def get_queryset(self):
        house_id = self.kwargs.get('house_id')
        return Resident.objects.filter(
            ownerships__apartment__house_id=house_id
        ).distinct().prefetch_related(
            'ownerships__apartment__house',
            'cars',
            'reserved_parking_spaces'
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['house_id'] = self.kwargs.get('house_id')
        return context


class ResidentCreateView(generics.CreateAPIView):
    """Представление для создания нового жильца"""
    serializer_class = ResidentCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['house_id'] = self.kwargs.get('house_id')
        return context



