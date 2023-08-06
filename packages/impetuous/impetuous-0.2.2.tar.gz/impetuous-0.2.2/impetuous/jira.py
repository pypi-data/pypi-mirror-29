import asyncio
import contextlib
import logging

import attr

from impetuous.ext import (
    Submission,
    SubmissionStatus,
    LudicrousConditions,
    API,
    SECRET,
)


logger = logging.getLogger(__name__)


class JiraSubmission(dict, Submission):

    def __init__(self, issue, body):
        self.issue = issue
        super().__init__(body)

    @property
    def label(self):
        return self.issue

    def status(self, unit):
        status = super().status(unit)
        if status is SubmissionStatus.unsubmitted:
            if self.label in unit.post_results.get('jira', {}):
                return SubmissionStatus.submitted
            else:
                return SubmissionStatus.unsubmitted
        else:
            return status

    def update_submitted_unit(self, unit, result):
        unit_results = unit.post_results.setdefault('jira', {})
        assert self.issue not in unit_results, ('%r not expected in %r' % (self.issue, unit_results))
        unit_results[self.issue] = result


@attr.s(frozen=True)
class Jira(API):

    IDENTIFIER = 'jira'
    pattern = attr.ib()
    server = attr.ib()
    basic_auth = attr.ib(metadata={SECRET: True},
                         convert=lambda value: tuple(value.split(':', 1)))

    def discover(self, impetuous, *units):
        for unit in units:
            for match in self.discover_by_pattern(unit, self.pattern):
                yield unit, JiraSubmission(match, {
                    'started': unit.start.strftime('%Y-%m-%dT%H:%M:%S.000%z'),
                    'timeSpentSeconds': unit.duration_in_minutes * 60,
                    'comment': unit.full_comment,
                })

    async def agent(self, impetuous):
        return JiraHttpAgent(self)


class JiraHttpAgent(object):

    def __init__(self, api):
        import aiohttp
        self.api = api
        self.sess = aiohttp.ClientSession(auth=aiohttp.BasicAuth(*api.basic_auth))
        self.close = self.sess.close

    async def submit(self, sub):
        import aiohttp
        where = self.api.server + '/rest/api/2/issue/{}/worklog'.format(sub.issue)
        resp = await self.sess.post(where, json=sub, params={'notifyUsers': 'false'})
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError as e:
            raise LudicrousConditions(e, "While submitting to {}: {}".format(resp.request_info.url, await resp.text()))
        else:
            return await resp.json()
