from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from versions.views import VersionViewSet

version_router = SimpleRouter()
version_router.register(r'', VersionViewSet, base_name='version')

urlpatterns = [
    url(r'', include(version_router.urls, namespace='api')),
]
