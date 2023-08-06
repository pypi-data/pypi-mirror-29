import contextlib
import datetime
import logging

import attr

from impetuous.sheet import format_comments
from impetuous.ext import (
    Submission,
    SubmissionStatus,
    LudicrousConditions,
    API,
    SECRET,
)


logger = logging.getLogger(__name__)


class FreshdeskSubmission(dict, Submission):

    def __init__(self, ticket_id, body):
        self.ticket_id = ticket_id
        super().__init__(body)

    @property
    def label(self):
        return self.ticket_id

    def status(self, unit):
        status = super().status(unit)
        if status is SubmissionStatus.unsubmitted:
            if self.label in unit.post_results.get('freshdesk', {}):
                return SubmissionStatus.submitted
            else:
                return SubmissionStatus.unsubmitted
        else:
            return status

    def update_submitted_unit(self, unit, result):
        unit_results = unit.post_results.setdefault('freshdesk', {})
        assert self.ticket_id not in unit_results, ('%r not expected in %r' % (self.ticket_id, unit_results))
        unit_results[self.ticket_id] = result


@attr.s(frozen=True)
class Freshdesk(API):

    IDENTIFIER = 'freshdesk'
    pattern = attr.ib()
    server = attr.ib()
    api_key = attr.ib(metadata={SECRET: True})

    def discover(self, impetuous, *units):
        for unit in units:
            time_spent = '%02i:%02i' % divmod(unit.duration_in_minutes, 60)
            for match in self.discover_by_pattern(unit, self.pattern):
                yield unit, FreshdeskSubmission(match, {
                    'time_spent': time_spent,
                    'executed_at': unit.start.astimezone(datetime.timezone.utc).isoformat(),
                    'note': format_comments([c for c in unit.comments if '[billable]' not in c]),
                    'billable': '[billable]' in unit.full_comment,
                    'timer_running': not 'if I have anything to do with it',
                })

    async def agent(self, impetuous):
        return FreshdeskHttpAgent(self)


class FreshdeskHttpAgent(object):

    def __init__(self, api):
        import aiohttp
        self.api = api
        self.sess = aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.api.api_key, 'X'))
        self.close = self.sess.close

    async def submit(self, sub):
        import aiohttp
        where = self.api.server + '/api/v2/tickets/{}/time_entries'.format(sub.ticket_id)
        resp = await self.sess.post(where, json=sub)
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError as e:
            raise LudicrousConditions(e, "While submitting to {}: {}".format(resp.request_info.url, await resp.text()))
        else:
            return await resp.json()
