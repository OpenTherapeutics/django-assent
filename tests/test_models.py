# -*- coding: utf-8 -*-

import pytest

from assent.models import Agreement, AgreementUser, AgreementVersion


@pytest.mark.django_db
class TestAgreement:
    def test_str(self, publication):
        assert str(publication) == 'test'

class TestAgreementVersion():
    def test_str(self, agreement_version):
        assert str(agreement_version) == 'Agreement: "test key" released: 2017-01-02 12:34'
