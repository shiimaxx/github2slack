from datetime import datetime
import unittest

from github2slack import fetch_unread_notifications


NOTIFICATIONS = (
    {
        'repository': {'name': 'github2slack'},
        'subject': {'title': 'pre-release'},
        'unread': True,
        'updated_at': datetime(2018, 1, 1, 0, 0),
        'url': 'https:example.com/notification/threads/100000000'
    },
    {
        'repository': {'name': 'github2slack'},
        'subject': {'title': 'Feature/logging'},
        'unread': True,
        'updated_at': datetime(2018, 1, 1, 1, 25),
        'url': 'https:example.com/notification/threads/100000001'
    },
    {
        'repository': {'name': 'github2slack'},
        'subject': {'title': 'Refactoring'},
        'unread': False,
        'updated_at': datetime(2018, 1, 5, 10, 5),
        'url': 'https:example.com/notification/threads/100000004'
    },
    {
        'repository': {'name': 'pocket'},
        'subject': {'title': 'Add test'},
        'unread': True,
        'updated_at': datetime(2018, 1, 2, 13, 23),
        'url': 'https:example.com/notification/threads/100000002'
    },
    {
        'repository': {'name': 'dynamic-route53'},
        'subject': {'title': 'development'},
        'unread': False,
        'updated_at': datetime(2018, 1, 5, 3, 45),
        'url': 'https:example.com/notification/threads/100000003'
    }
)


class TestGithub2Slack(unittest.TestCase):
    def test_fetch_unread_notification(self):
        unread_notifications = fetch_unread_notifications()
        self.assertEqual(2, len(unread_notifications['github2slack']))
        self.assertEqual(1, len(unread_notifications['pocket']))
        self.assertNotIn('dynamic-route53', unread_notifications.keys())
