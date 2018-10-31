from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from . import views

app_name = 'authentication'
router = DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='authentication-user')
urlpatterns = router.urls
