from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers


# django rest framework router
router = routers.DefaultRouter()
# end of django rest framework router

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#    url(r'^api/v1/', include('signals.apps.entities_2.api_v1.urls',namespace='v1')),
    url(r'^api/v1/', include('signals.apps.entities.api_v1.urls',namespace='v1')),
    url(r'^admin/', admin.site.urls),
]
