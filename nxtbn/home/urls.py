from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from nxtbn.home import views as home_views


urlpatterns = [
    path('', home_views.home, name='home'),
    path('admin/', home_views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)