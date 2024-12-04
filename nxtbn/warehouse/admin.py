from django.contrib import admin
from nxtbn.warehouse.models import Stock, Warehouse, StockMovement
# Register your models here.


admin.site.register(Stock)
admin.site.register(Warehouse)
admin.site.register(StockMovement)