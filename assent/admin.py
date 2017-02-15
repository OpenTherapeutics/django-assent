# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.utils.translation import ugettext as _

from transcode.conf import get_content_formatters

from .models import Agreement, AgreementUser, AgreementVersion

ContentFormat = get_content_formatters('ASSENT_FORMATTERS')


# ===== INLINES ===============================================================

class AgreementVersionForm(forms.ModelForm):
    content_format = forms.ChoiceField(
        label=_('Content Format'), required=True, choices=ContentFormat.CHOICES)

    class Meta:
        model = AgreementVersion
        fields = (
            'short_title',
            'full_title',
            'content',
            'content_format',
        )

    def __init__(self, *args, **kwargs):
        super(AgreementVersionForm, self).__init__(*args, **kwargs)
        instance = self.instance
        if not instance or not instance.content_format:
            self.fields['content_format'].initial = ContentFormat.DEFAULT


class AgreementVersionInlineAdmin(admin.StackedInline):
    model = AgreementVersion
    extra = 0
    readonly_fields = ('release_date', )
    form = AgreementVersionForm
    fieldsets = (
        (None, {
            'fields': (
                'short_title',
                'full_title',
                'content',
                'content_format',
                'release_date',
            )
        }),
    )

# ===== ADMINS ================================================================


class AgreementAdmin(admin.ModelAdmin):
    inlines = (AgreementVersionInlineAdmin, )
    prepopulated_fields = {"slug": ("document_key",)}
    fieldsets = (
        (None, {
            'fields': (
                'document_key',
                'slug',
                'description',
                'short_description',
                'latest_version',
            )
        }),
    )


admin.site.register(Agreement, AgreementAdmin)


class AgreementUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'agreement_version', 'acceptance_date', )
    readonly_fields = ('acceptance_date', 'ip_address', )
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'agreement_version',
                'acceptance_date',
                'ip_address',
            )
        }),
    )


admin.site.register(AgreementUser, AgreementUserAdmin)
