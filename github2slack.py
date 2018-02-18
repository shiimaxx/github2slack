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
    return github_.get_user().get_notifications()


def _fetch_html_url(notification):
    req = Request(notification.subject.latest_comment_url)
    try:
        res = urlopen(req)
    except HTTPError as error_:
        logger.error(error_)

    body = res.read()
    loads_json = json.loads(body.decode('utf-8'))
    return loads_json['html_url']


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
                    'url': _fetch_html_url(notification)
                }
            )

    return unread_notifications


def make_post_text(unread_notifications):
    post_text = ''
    for repository in unread_notifications.keys():
        post_text += "*{}*\n".format(repository)
        for notification in unread_notifications[repository]:
            post_text += "`{}` {}\n".format(notification['subject'], notification['url'])
        post_text += '\n'
    return post_text.rstrip()


def _make_request(post_text):
    payload = {'text': post_text}
    return Request(HOOK_URL, json.dumps(payload).encode('utf-8'))


def post(post_text):
    req = _make_request(post_text)
    try:
        urlopen(req)
    except HTTPError as error_:
        logger.error(error_)


def main():
    unread_notifications = fetch_unread_notifications()
    post_text = make_post_text(unread_notifications)
    post(post_text)


if __name__ == '__main__':
    main()
