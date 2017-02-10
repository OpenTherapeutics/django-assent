# -*- coding: utf-8 -*-

import datetime
import os
import pytest
import pytz

from django import setup
from django.contrib.auth import get_user_model

from assent.models import Agreement, AgreementUser, AgreementVersion


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')
    setup()


@pytest.fixture
def user():
    obj = get_user_model.create(email='test@test.com', username='test_user')
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
def version(agreement):
    obj = AgreementVersion.objects.create(
        agreement=agreement,
        short_title='test version',
        full_title='test version',
        content='test version',
        content_format='TEXT',
        release_date=datetime.datetime(2017, 1, 2, 12, 34, 56).replace(tzinfo=pytz.utc),
    )
    agreement.latest_version = obj
    agreement.date_modified = obj.release_date
    agreement.save()
    return obj
