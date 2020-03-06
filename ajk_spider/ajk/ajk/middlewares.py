# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random


class UserAgentDownLoadMildeware(object):

    def __init__(self, user_agent_list):
        self.user_agent = user_agent_list

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        middleware = cls(crawler.settings.get('USER_AGENT_LIST'))
        return middleware

    def process_request(self, request, spider):
        print('this is request user_agent' + random.choice(self.user_agent))
        request.headers['user-agent'] = random.choice(self.user_agent)
