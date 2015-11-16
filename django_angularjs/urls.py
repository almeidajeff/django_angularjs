# -*- coding:utf-8 -*-
# Imports
from rest_framework_nested import routers

from authentication.views import AccountViewSet

from django.conf.urls import patterns, url
from django_angularjs.views import IndexView

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = patterns(
    '',
    # URLs
    url(r'^api/v1/', include(router.urls)),
    url('^.*$', IndexView.as_view(), name='index'),
)
