from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        
        if self.request.user.user_type == 'manager':
            keyword = self.request.query_params.get('q', None)
            
            if keyword:
                return queryset.filter(
                    Q(email__icontains=keyword) | 
                    Q(first_name__icontains=keyword) | 
                    Q(last_name__icontains=keyword)
                )
            else:
                return queryset
        
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
