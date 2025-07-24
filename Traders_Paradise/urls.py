from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from bots import views as bots_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Bots app
    path('bots/', include('bots.urls')),

    # Homepage
    path('', bots_views.homepage, name='homepage'),

    # Login & Logout
    path('login/', auth_views.LoginView.as_view(template_name='bots/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
