import re
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls', namespace='users')),
    path('api/recipe/', include('recipe.urls', namespace='recipe')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user/password/reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),
]
#     re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^(?!api/).*$', RedirectView.as_view(url='/static/index.html', permanent=False)),
]

# Media Assets
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Schema URLs
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),
    # path('build', )
    # re_path(r'^.*$', serve, kwargs={'path': 'index.html'}),
    # path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]