# -*- coding: utf-8 -*-

import os
import pytest

from django import setup
from django.utils import timezone
from django.contrib.auth import get_user_model

from assent.models import Agreement, AgreementUser, AgreementVersion


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')
    setup()


@pytest.fixture
def user():
    obj = get_user_model().objects.create(email='test@test.com', username='test_user')
    return obj


@pytest.fixture
def agreement():
    obj = Agreement.objects.create(
        document_key='test key',
        description='test description',
        short_description='test short description',
        latest_version=None,
        date_modified=None,
    )
    return obj


@pytest.fixture
def agreement_version(agreement):
    obj = AgreementVersion.objects.create(
        agreement=agreement,
        short_title='test version',
        full_title='test version',
        content='test content',
        content_format='TEXT',
        release_date=None,
    )
    agreement.latest_version = obj
    agreement.date_modified = obj.release_date
    agreement.save()
    return obj


@pytest.fixture
def agreement_user(agreement_version, user):
    acceptance_date = timezone.now()
    obj = AgreementUser.objects.create(
        user=user,
        agreement_version=agreement_version,
        acceptance_date=acceptance_date,
        ip_address='2001:db8:85a3:0:0:8a2e:370:7334'
    )
    return obj
