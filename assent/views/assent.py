# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from ..models import Agreement, AgreementUser
from .forms import AgreementForm


@method_decorator(login_required, name='dispatch')
class AgreementListView(ListView):
    model = AgreementUser
    template_name = 'assent/agreement_list.html'

    def get_queryset(self):
        """
        Override to use the user from the request as part of the query.
        """
        queryset = super(AgreementListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class AgreementMixin(object):
    @cached_property
    def agreement(self):
        """
        Returns the Agreement specified in the url
        """
        slug = self.kwargs.get('slug', None)
        return get_object_or_404(Agreement, slug=slug)

    def get_object(self, queryset=None):
        agreement_version = self.agreement.latest_version
        if queryset is None:
            queryset = self.get_queryset()
        obj = queryset.filter(
            user=self.request.user, agreement_version=agreement_version).first()
        return obj

    def get_context_data(self, **kwargs):
        """
        Ensures agreement and its latest_version are in the context.
        """
        context = super(AgreementMixin, self).get_context_data(**kwargs)
        context['agreement'] = self.agreement
        context['agreement_version'] = self.agreement.latest_version
        return context


@method_decorator(login_required, name='dispatch')
class AgreementDetailView(AgreementMixin, DetailView):
    model = AgreementUser
    template_name = 'assent/agreement_detail.html'


@method_decorator(login_required, name='dispatch')
class AgreementFormView(AgreementMixin, SingleObjectTemplateResponseMixin,
                        ModelFormMixin, ProcessFormView):
    """
    This is essentially a CreateOrUpdateView. If the object dosn't exist, it is
    created. If it already does, then it is updated.
    """
    model = AgreementUser
    template_name = 'assent/agreement_form.html'
    form_class = AgreementForm
    success_url = reverse_lazy('assent:agreement_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AgreementFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AgreementFormView, self).post(request, *args, **kwargs)

    @cached_property
    def client_ip_address(self):
        """
        Attempts to return the user's IP address.
        :return:
        """
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({
            'user': self.request.user,
            'agreement_version': self.agreement.latest_version,
            'acceptance_date': timezone.now(),
            'ip_address': self.client_ip_address,
        })
        return initial
