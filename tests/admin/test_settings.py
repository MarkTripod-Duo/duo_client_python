import json
from .. import util
import duo_client.admin
from .base import TestAdmin


class TestSettings(TestAdmin):

    def test_update_settings(self):
        """ Test updating settings
        """
        self.maxDiff = None
        response = self.client_list.update_settings(
            lockout_threshold=10,
            lockout_expire_duration=60,
            inactive_user_expiration=30,
            pending_deletion_days=5,
            log_retention_days=180,
            sms_batch=5,
            sms_expiration=60,
            sms_refresh=True,
            sms_message='test_message',
            fraud_email='test@example.com',
            fraud_email_enabled=True,
            keypress_confirm='0',
            keypress_fraud='9',
            timezone='UTC',
            telephony_warning_min=50,
            caller_id='+15035551000',
            user_telephony_cost_max=10,
            minimum_password_length=12,
            password_requires_upper_alpha=True,
            password_requires_lower_alpha=True,
            password_requires_numeric=True,
            password_requires_special=True,
            helpdesk_bypass="allow",
            helpdesk_bypass_expiration=60,
            helpdesk_message="test_message",
            helpdesk_can_send_enroll_email=True,
            security_checkup_enabled=True,
            user_managers_can_put_users_in_bypass=False,
            email_activity_notification_enabled=True,
            push_activity_notification_enabled=True,
            unenrolled_user_lockout_threshold=100,
            enrollment_universal_prompt_enabled=True,
        )
        response = response[0]
        self.assertEqual(response['method'], 'POST')
        self.assertEqual(response['uri'], '/admin/v1/settings')
        self.assertEqual(
            json.loads(response['body']),
            {
                'account_id': self.client.account_id,
                'lockout_threshold': '10',
                'lockout_expire_duration': '60',
                'inactive_user_expiration': '30',
                'log_retention_days': '180',
                'sms_batch': '5',
                'sms_expiration': '60',
                'sms_refresh': '1',
                'sms_message': 'test_message',
                'fraud_email': 'test@example.com',
                'fraud_email_enabled': '1',
                'keypress_confirm': '0',
                'keypress_fraud': '9',
                'timezone': 'UTC',
                'telephony_warning_min': '50',
                'caller_id': '+15035551000',
                'user_telephony_cost_max': '10',
                'pending_deletion_days': '5',
                'minimum_password_length': '12',
                'password_requires_upper_alpha': '1',
                'password_requires_lower_alpha': '1',
                'password_requires_numeric': '1',
                'password_requires_special': '1',
                'helpdesk_bypass': 'allow',
                'helpdesk_bypass_expiration': '60',
                'helpdesk_message': 'test_message',
                'helpdesk_can_send_enroll_email': '1',
                'security_checkup_enabled': '1',
                'user_managers_can_put_users_in_bypass': '0',
                'email_activity_notification_enabled': '1',
                'push_activity_notification_enabled': '1',
                'unenrolled_user_lockout_threshold': '100',
                'enrollment_universal_prompt_enabled': '1',
            })
