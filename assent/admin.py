# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Agreement, AgreementUser, AgreementVersion


# ===== INLINES ===============================================================

class AgreementVersionInlineAdmin(admin.StackedInline):
    model = AgreementVersion
    extra = 0
    readonly_fields = ('release_date', )
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
    fieldsets = (
        (None, {
            'fields': (
                'document_key',
                'description',
                'short_description',
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
