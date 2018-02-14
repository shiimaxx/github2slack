#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger, INFO
import os

from github import Github

logger = getLogger()
logger.setLevel(INFO)

GITHUB_USER = os.getenv('GITHUB_USER', default=None)
GITHUB_PASSWORD = os.getenv('GITHUB_PASSWORD', default=None)


def _fetch_notifications():
    if GITHUB_USER is None or GITHUB_PASSWORD is None:
        logger.error('Set "GITHUB_USER" and "GITHUB_PASSWORD for environ variables is required')
        return
    github_ = Github(GITHUB_USER, GITHUB_PASSWORD)
    return github_.getuser().get_notifications().get_page(0)


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
                    'updated_at': notification.updated_at,
                    'url': notification.url
                }
            )

    return unread_notifications
