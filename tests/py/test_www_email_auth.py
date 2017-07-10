# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json

from gratipay.testing import Harness
from gratipay.testing.email import QueuedEmailHarness


class TestSendLink(Harness):
    def test_returns_json(self):
        self.make_participant('alice', email_address='alice@gratipay.com')
        response = self.client.POST('/auth/email/send_link.json', {'email_address': 'alice@gratipay.com'})

        message = json.loads(response.body)['message']
        assert message == "We've sent you a link to sign in. Please check your inbox."

    def test_only_allows_post(self):
        response = self.client.GxT('/auth/email/send_link.json')

        assert response.code == 405

    def test_400_for_no_email_address_parameter(self):
        response = self.client.PxST('/auth/email/send_link.json')

        assert response.code == 400

    def test_400_for_invalid_email(self):
        response = self.client.PxST('/auth/email/send_link.json', {'email_address': 'dummy@gratipay.com'})

        # TODO: Change this when signup links are supported

        assert response.code == 400

class TestSendLinkEmail(QueuedEmailHarness):
    def test_sends_email(self):
        self.make_participant('alice', email_address='alice@gratipay.com')
        self.client.POST('/auth/email/send_link.json', {'email_address': 'alice@gratipay.com'})

        assert self.get_last_email()['to'] == 'alice <alice@gratipay.com>'
        assert 'Click the link below to sign in to Gratipay' in self.get_last_email()['body_text']
        assert 'Click the button below to sign in to Gratipay' in self.get_last_email()['body_html']
