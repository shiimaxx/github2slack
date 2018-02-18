#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

from logging import getLogger, INFO
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from github import Github

logger = getLogger()
logger.setLevel(INFO)

GITHUB_USER = os.getenv('GITHUB_USER', default=None)
GITHUB_PASSWORD = os.getenv('GITHUB_PASSWORD', default=None)
HOOK_URL = os.getenv('HOOK_URL', default=None)


def _fetch_notifications():
    if GITHUB_USER is None or GITHUB_PASSWORD is None:
        logger.error('Set "GITHUB_USER" and "GITHUB_PASSWORD for environ variables is required')
        return
    github_ = Github(GITHUB_USER, GITHUB_PASSWORD)
    return github_.getuser().get_notifications()


def fetch_unread_notifications():
    notifications = _fetch_notifications()

    unread_notifications = {}
    for notification in notifications:
        if notification.unread:
            repository_name = notification.repository.name
            if repository_name not in unread_notifications.keys():
                unread_notifications[repository_name] = []
            unread_notifications[repository_name].append(
                {
                    'subject': notification.subject.title,
                    'updated_at': notification.updated_at.strftime('%Y/%m/%d %H:%M'),
                    'url': notification.url
                }
            )

    return unread_notifications


def make_posts_text(unread_notifications):
    posts_text = ''
    for repository in unread_notifications.keys():
        posts_text += "*{}*\n".format(repository)
        for notification in unread_notifications[repository]:
            posts_text += "`{}` {}\n".format(notification['subject'], notification['url'])
        posts_text += '\n'
    return posts_text.rstrip()


def _make_request(posts_text):
    payload = {'text': posts_text}
    return Request(HOOK_URL, json.dumps(payload).encode('utf-8'))


def post(posts_text):
    req = _make_request(posts_text)
    try:
        urlopen(req)
    except HTTPError as error_:
        logger.error(error_)


def main():
    unread_notifications = fetch_unread_notifications()
    posts_text = make_posts_text(unread_notifications)
    post(posts_text)


if __name__ == '__main__':
    main()
