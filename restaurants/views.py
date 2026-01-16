from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour consulter les restaurants.
    
    Filtres disponibles:
    - ?cuisine=italien : Filtrer par cuisine
    - ?search=nom : Rechercher par nom
    - ?min_rating=4.0 : Note minimale
    - ?ordering=-rating : Trier par note décroissante
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'cuisine', 'address']
    filterset_fields = ['cuisine']
    ordering_fields = ['rating', 'reviews', 'name', 'created_at']
    ordering = ['-rating', '-reviews']
    
    @action(detail=False, methods=['get'])
    def cuisines(self, request):
        """Liste toutes les cuisines disponibles"""
        cuisines = Restaurant.objects.values_list('cuisine', flat=True).distinct().order_by('cuisine')
        return Response({'cuisines': list(cuisines)})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques globales"""
        total = Restaurant.objects.count()
        cuisines_count = Restaurant.objects.values('cuisine').distinct().count()
        avg_rating = Restaurant.objects.aggregate(
            avg_rating=models.Avg('rating')
        )['avg_rating']
        
        return Response({
            'total_restaurants': total,
            'total_cuisines': cuisines_count,
            'average_rating': round(avg_rating, 2) if avg_rating else None,
        })
