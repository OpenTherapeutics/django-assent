# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from choice_enum import Option, make_enum_class

from transcode.render import render as transcode_render


# Converts the ASSENT_FORMATTERS setting to a ChoiceEnum
_choice_enum_kwargs = {
    k: Option(k, v['label'], default='default' in v) for k, v in
    settings.ASSENT_FORMATTERS.items()}
ContentFormat = make_enum_class('ContentFormat', **_choice_enum_kwargs)


class Agreement(models.Model):
    document_key = models.CharField(
        _('document key'), max_length=255, blank=False, default='',
        unique=True)
    description = models.CharField(
        _('description'), max_length=4096, blank=False, default='')
    short_description = models.CharField(
        _('short description'), max_length=255, blank=False, default='')

    latest_version = models.OneToOneField(
        'assent.AgreementVersion', blank=True, null=True, related_name='+')
    # Note, this should only be updated when we add a new version
    # This is currently done in AgreementVersion.save()
    date_modified = models.DateTimeField(
        default=timezone.now, blank=True, null=True, editable=False)

    class Meta:
        verbose_name = _('agreement')
        verbose_name_plural = _('agreements')

    def __str__(self):
        return self.document_key


class AgreementUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    agreement_version = models.ForeignKey(
        to='assent.AgreementVersion',
        verbose_name=_('agreement_version'),
        related_name='agreement_users', blank=False)
    acceptance_date = models.DateTimeField(
        _('acceptance date'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(
        _('IP address'), blank=True, null=True)

    class Meta:
        verbose_name = _('agreement user')
        verbose_name_plural = _('agreement users')

    def __str__(self):
        return _('User: {0}, agreement: {1}').format(
            self.user, self.agreement_version)


class AgreementVersion(models.Model):
    users = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, through='assent.AgreementUser',
        related_name='agreement_versions', verbose_name=_('users'))
    agreement = models.ForeignKey(
        to='assent.Agreement', verbose_name=_('agreement'),
        related_name='versions', blank=False)
    short_title = models.CharField(
        _('short title'), max_length=255, blank=False, default='')

    full_title = models.CharField(
        _('full title'), max_length=1023, blank=False, default='')
    content = models.TextField(
        _('content'), blank=True, default='')
    content_format = models.CharField(
        _('content format'), max_length=8, choices=ContentFormat.CHOICES,
        default=ContentFormat.DEFAULT, blank=False)
    release_date = models.DateTimeField(
        _('release date'), auto_now_add=True)

    class Meta:
        get_latest_by = ('release_date', )
        ordering = ('-release_date', )
        verbose_name = _('agreement version')
        verbose_name_plural = _('agreement versions')

    def __str__(self):
        return _('Agreement: "{0}" released: {1:%Y-%m-%d %H:%M}').format(
            self.agreement.document_key, self.release_date)

    def get_rendered_content(self):
        return transcode_render(self.content, self.content_format)

    def save(self, *args, **kwargs):
        super(AgreementVersion, self).save(*args, **kwargs)
        if self.pk is not None:
            if self.agreement:
                self.agreement.latest_version = self
                self.agreement.date_modified = self.release_date
                self.agreement.save()
