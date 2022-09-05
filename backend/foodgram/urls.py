from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls', namespace='users')),
    path('api/', include('recipes.urls', namespace='recipes')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

