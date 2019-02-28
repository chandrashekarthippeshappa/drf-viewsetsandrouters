from django.urls import path,include
from django.conf.urls import url

from . import views

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'groups', views.GroupsViewSet,base_name='groups')
router.register(r'group', views.GroupDetailsViewSet,base_name='group')
router.register(r'logout', views.LogoutViewSet,base_name='logout')
router.register(r'photos',views.GroupPhotosViewSet,base_name='photos')
router.register(r'photo', views.PhotoViewSet,base_name='photo')
router.register(r'login', views.LoginViewSet,base_name='login')

urlpatterns = [
    url(r'^', include(router.urls)),

]
