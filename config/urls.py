from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('account/',include('account.urls')),
    path('payement/',include('payement.urls')),
    path('tontine/',include('tontine.urls')),
    path('',include('blog.urls')),
    path('admin_tontine/',include('admin_tontine.urls')),
    path('tontine_individuelle/',include('tontine_individuelle.urls')),
    path('user-tontine/',include('user_tontine.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

