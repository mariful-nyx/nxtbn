from rest_framework import generics
from nxtbn.core.paginator import NxtbnPagination
from nxtbn.discount.models import PromoCode
from .serializers import PromoCodeSerializer

class PromoCodeListCreateAPIView(generics.ListCreateAPIView):
    pagination_class = NxtbnPagination
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer


class PromoCodeUpdateRetrieveDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    lookup_field = 'id'