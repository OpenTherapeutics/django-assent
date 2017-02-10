# -*- coding: utf-8 -*-

import pytest


@pytest.mark.django_db
class TestAgreement:
    def test_str(self, agreement):
        assert str(agreement) == 'test key'


@pytest.mark.django_db
class TestAgreementVersion:
    def test_str(self, agreement_version):
        timestamp = agreement_version.release_date
        assert str(agreement_version) == 'Agreement: "test key" released: {0:%Y-%m-%d %H:%M}'.format(timestamp)

    def test_plain_text_render(self, agreement_version):
        assert agreement_version.get_rendered_content() == '<p>test content</p>'


@pytest.mark.django_db
class TestAgreementUser:
    def test_str(self, agreement_version, agreement_user, user):
        # Assign user to having signed the agreement
        assert str(agreement_user) == "User: {0}, agreement: {1}".format(
            user, agreement_version)

    def test_relationships(self, agreement_user, agreement_version, user):
        assert agreement_version in list(user.agreement_versions.all())
        assert user in list(agreement_version.users.all())
