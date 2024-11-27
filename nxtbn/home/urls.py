from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from nxtbn.home import views as home_views


urlpatterns = [
    path('', home_views.home, name='home'),
    path('admin/', home_views.nxtbn_admin, name='nxtbn_admin'),
    path('upload-admin/', home_views.upload_admin, name='upload_admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)