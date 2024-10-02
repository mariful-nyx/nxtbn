from django.urls import path
from nxtbn.tax.api.dashboard.views import (
    TaxClassView, 
    TaxClassDetailsView, 
    TaxRateListCreateAPIView, 
    TaxRateRetrieveUpdateDelete
)

urlpatterns = [
    path('tax-class/', TaxClassView.as_view(), name='tax-class-list-create'),
    path('tax-class/<int:id>/', TaxClassDetailsView.as_view(), name='tax-class-detail'),
    path('tax-rates/', TaxRateListCreateAPIView.as_view(), name='tax-rates-by-tax-class'),
    path('tax-rates/<int:id>/', TaxRateRetrieveUpdateDelete.as_view(), name='tax-rates-retrieve-update-delete')

]
