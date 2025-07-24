from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bots import views as bots_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bots/', include('bots.urls')),
    path('', bots_views.homepage, name='homepage'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
