from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
import logging
import re

import attr

from impetuous.config import CodedValue

logger = logging.getLogger(__name__)

SECRET = 'secret'  # Mark configuration values as secrets, for encoding/decoding


class LudicrousConditions(RuntimeError):
    """
    Raise when when the module can't complete a request due invalid state like
    incomplete configuration or the weather or something. The program may
    display your error and quit or ignore it.
    """

    def __init__(self, error, suggestion):
        self.error = error
        self.suggestion = suggestion


class ConfigRequired(LudicrousConditions):

    @classmethod
    def from_attrs(cls, exc, other, section):
        setme = ", ".join(f"`{field.name}`" for field in attr.fields(other))
        return cls(exc, f"Maybe edit your config and set, {setme}, under the `[{section}]` section.")



class SubmissionStatus(Enum):

    invalid = 0
    unsubmitted = 1
    submitted = 2


class API(ABC):

    @abstractproperty
    def IDENTIFIER(self):
        """ A short string to pick this guy out of a crowd ...
        """

    @abstractmethod
    def discover(self, impetuous, *units):
        """ yield (unit, Submission) pairs.
        """

    @abstractmethod
    async def agent(self, impetuous, ext):
        """
        Produce an object with a submit(Submission) coroutine method that can
        submit submissions to the given `ext`.
        """

    @classmethod
    def from_somewhere(cls, impetuous, section):
        return cls.from_config(impetuous.get_config_or_empty(), section)

    @classmethod
    def coded_fields(cls):
        return [field for field in attr.fields(cls) if field.metadata.get(SECRET)]

    @classmethod
    def from_config(cls, section):
        try:
            return cls(**{
                field.name:
                    CodedValue.decode_from_config(section, field.name)
                    if field.metadata.get(SECRET)
                    else section[field.name]
                for field in attr.fields(cls)
            })
        except KeyError as e:
            raise ConfigRequired.from_attrs('Key missing: %s' % e, cls, section.name)

    def discover_by_pattern(self, unit, pattern):
        logger.debug(_("%s looking for matches in %r using pattern %s."), type(self).__name__, unit.task, pattern)
        for match in re.findall(pattern, unit.task):
            logger.debug(_("%s found %r in %r using pattern %s."), type(self).__name__, match, unit.task, pattern)
            yield match


class Submission(ABC):

    @property
    def label(self):
        """Short but readable label to identify the submission."""
        return type(self).__name__

    def status(self, unit) -> SubmissionStatus:
        if unit.covert:
            return SubmissionStatus.invalid
        elif unit.end is None:
            return SubmissionStatus.invalid
        elif unit.duration.total_seconds() <= 0:
            return SubmissionStatus.invalid
        elif unit.duration.total_seconds() < 60:
            logger.warning(_("%s has fewer than 60 seconds of time logged. JIRA/things will lose their minds I try to log this."), unit.task)
            return SubmissionStatus.invalid
        else:
            return SubmissionStatus.unsubmitted

    @abstractmethod
    def update_submitted_unit(self, unit, submission, result):
        """
        Modify the given unit such that the status() know that it is submitted
        if it were called after this.

        result may be a FakeSubmissionResult if a dry run thingy is going on.
        """


@attr.s(frozen=True)
class Ext(object):
    """
    Modules allow for talking to external APIs so you can post time to JIRA or
    Freshdesk or whatever.

    #They shouldn't be too slow, as they may be created and run frequently, such
    #as whenever a unit is printed.
    """
    api = attr.ib()
    abbr = attr.ib()
    name = attr.ib()
