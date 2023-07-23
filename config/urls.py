from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView


scheam_view = get_schema_view(
    openapi.Info(
        title = "LMS APIs",
        desciption = "Learning Managment System",
        default_version = "1.0.0.0",
        terms_of_service = "",
    ),
    public = True,
    permission_classes = (permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', scheam_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('user/', include('users_app.urls')),
    path('', TemplateView.as_view(template_name='base.html'), name='base'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
