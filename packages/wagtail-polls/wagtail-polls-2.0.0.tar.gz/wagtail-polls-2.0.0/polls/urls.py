from django.conf.urls import url, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'polls', views.PollViewSet, base_name='polls')
router.register(r'vote', views.VoteViewSet, base_name='vote')

urlpatterns = [
    url(r'api/', include(router.urls)),
]
