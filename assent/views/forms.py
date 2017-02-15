# -*- coding: utf-8 -*-

from django import forms

from ..models import AgreementUser


class AgreementForm(forms.ModelForm):
    hidden_fields = (
        'user', 'agreement_version', 'ip_address', 'acceptance_date', )

    class Meta:
        model = AgreementUser
        fields = (
            'user', 'agreement_version', 'ip_address', 'acceptance_date', )

    def __init__(self, *args, **kwargs):
        """
        Hides any fields listed in the class property: hidden_fields.
        """
        super(AgreementForm, self).__init__(*args, **kwargs)
        for fld in self.hidden_fields:
            self.fields[fld].widget = forms.widgets.HiddenInput()
