from django.urls import path
from nxtbn.tax.api.dashboard.views import TaxClassView, TaxClassRetrieveUpdateDelete

urlpatterns = [
    path('tax-class/', TaxClassView.as_view(), name='tax-class-list-create'),
    path('tax-class/<int:id>/', TaxClassRetrieveUpdateDelete.as_view(), name='tax-class-detail')

]
