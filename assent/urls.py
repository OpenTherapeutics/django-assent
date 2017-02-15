# -*- coding: utf-8 -*-

from django.conf.urls import url, include


from .views import (
    AgreementDetailView,
    AgreementListView,
    AgreementFormView,
)


urlpatterns = [
    url(r'^$', AgreementListView.as_view(), name='agreement_list'),
    url(r'^(?P<slug>[^/]+)/$', AgreementDetailView.as_view(), name='agreement_detail'),
    url(r'^(?P<slug>[^/]+)/accept/$', AgreementFormView.as_view(), name='agreement_form'),
]
