from datetime import datetime
import unittest
from unittest.mock import Mock, patch

from github2slack import fetch_unread_notifications, make_post_text


dummy_notification0 = Mock()
dummy_notification0.repository.name = 'github2slack'
dummy_notification0.subject.title = 'pre-release'
dummy_notification0.unread = True
dummy_notification0.updated_at = datetime(2018, 1, 1, 0, 0)
dummy_notification0.url = 'https://example.com/notification/threads/100000000'

dummy_notification1 = Mock()
dummy_notification1.repository.name = 'github2slack'
dummy_notification1.subject.title = 'Feature/logging'
dummy_notification1.unread = True
dummy_notification1.updated_at = datetime(2018, 1, 1, 1, 25)
dummy_notification1.url = 'https://example.com/notification/threads/100000001'

dummy_notification2 = Mock()
dummy_notification2.repository.name = 'github2slack'
dummy_notification2.subject.title = 'Refactoring'
dummy_notification2.unread = False
dummy_notification2.updated_at = datetime(2018, 1, 5, 10, 5)
dummy_notification2.url = 'https://example.com/notification/threads/100000002'

dummy_notification3 = Mock()
dummy_notification3.repository.name = 'pocket'
dummy_notification3.subject.title = 'Add test'
dummy_notification3.unread = True
dummy_notification3.updated_at = datetime(2018, 1, 5, 13, 23)
dummy_notification3.url = 'https://example.com/notification/threads/100000003'

dummy_notification4 = Mock()
dummy_notification4.repository.name = 'dynamic-route53'
dummy_notification4.subject.title = 'development'
dummy_notification4.unread = False
dummy_notification4.updated_at = datetime(2018, 1, 6, 3, 45)
dummy_notification4.url = 'https://example.com/notification/threads/100000004'

NOTIFICATIONS = (
    dummy_notification0,
    dummy_notification1,
    dummy_notification2,
    dummy_notification3,
    dummy_notification4
)


class TestGithub2Slack(unittest.TestCase):
    @patch('github2slack._fetch_notifications')
    def test_fetch_unread_notification(self, m):
        m.return_value = NOTIFICATIONS
        unread_notifications = fetch_unread_notifications()
        self.assertEqual(2, len(unread_notifications['github2slack']))
        self.assertEqual(1, len(unread_notifications['pocket']))
        self.assertNotIn('dynamic-route53', unread_notifications.keys())

        unread_github2slack_notification_subject = []
        unread_github2slack_notification_updated_at = []
        unread_github2slack_notification_url = []
        for notification in unread_notifications['github2slack']:
            unread_github2slack_notification_subject.append(notification['subject'])
            unread_github2slack_notification_updated_at.append(notification['updated_at'])
            unread_github2slack_notification_url.append(notification['url'])

        self.assertListEqual(['pre-release', 'Feature/logging'], unread_github2slack_notification_subject)
        self.assertListEqual(['2018/01/01 00:00', '2018/01/01 01:25'], unread_github2slack_notification_updated_at)
        self.assertListEqual([
            'https://example.com/notification/threads/100000000',
            'https://example.com/notification/threads/100000001'
        ], unread_github2slack_notification_url)

        self.assertEqual('Add test', unread_notifications['pocket'][0]['subject'])
        self.assertEqual('2018/01/05 13:23', unread_notifications['pocket'][0]['updated_at'])
        self.assertEqual('https://example.com/notification/threads/100000003', unread_notifications['pocket'][0]['url'])

    def test_make_post_text(self):
        unread_notifications = {
            'github2slack': [
                {
                    'subject': 'pre-release',
                    'updated_at': '2018/01/01 00:00',
                    'url': 'https://example.com/notification/threads/100000000'
                },
                {
                    'subject': 'Feature/logging',
                    'updated_at': '2018/01/01 01:25',
                    'url': 'https://example.com/notification/threads/100000001'
                }
            ],
            'pocket': [
                {
                    'subject': 'Add test',
                    'updated_at': '2018/01/05 13:23',
                    'url': 'https://example.com/notification/threads/100000003'
                },
            ]
        }

        post_text = make_post_text(unread_notifications)
        self.assertEqual("""*github2slack*
`pre-release` https://example.com/notification/threads/100000000
`Feature/logging` https://example.com/notification/threads/100000001

*pocket*
`Add test` https://example.com/notification/threads/100000003""", post_text)
