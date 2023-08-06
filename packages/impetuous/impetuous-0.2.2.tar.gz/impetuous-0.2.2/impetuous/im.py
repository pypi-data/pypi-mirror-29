from fnmatch import fnmatch
import logging

from impetuous.sheet import (
    SheetDirectory,
    Sheet,
    Unit,
    SheetNotFoundError,
    UnitNotFoundError,
    LinkNotFoundError,
    ValidationError,
    utcnow,
    localtz,
)
from impetuous.config import get_config
from impetuous.ext import LudicrousConditions, SubmissionStatus, Ext
from impetuous.jira import Jira
from impetuous.freshdesk import Freshdesk

logger = logging.getLogger(__name__)

NOT_EXT_SECTIONS = 'DEFAULT', 'impetuous'
API_CLASSES = {Jira.IDENTIFIER: Jira,
               Freshdesk.IDENTIFIER: Freshdesk}


class Impetuous(object):
    """ Base program behaviour. TODO dissolve into nothing...?
    """

    def __init__(self):
        try:
            self.config = get_config()
        except FileNotFoundError as e:
            logger.debug(_("Config could not be loaded: %r"), e)
            self.config = None
            self.config_error = e
        else:
            self.config_error = None

    def get_config_or_none(self):
        return self.config

    def get_config_or_empty(self):
        if self.config is None:
            return {}
        else:
            return self.config

    def get_config_or_quit(self):
        if self.config_error is not None:
            logger.error(self.config_error)
            logger.error(_("Try creating that file, see the readme for some ideas of what to put in it."))
            raise SystemExit(1)
        else:
            return self.config

    def get_unit_submissions(self, *units):
        """
        Returns a list of module, unit, submission tuples.
        Ordered by module and unit for easy grouping.
        """
        # TODO don't call this so often and cache the dumb thing better ...
        for __, ext in self.section_exts(self.get_config_or_quit()):
            try:
                for unit, submission in ext.api.discover(self, *units):
                    logger.debug(_("%s found submission %r."), ext.name, submission)
                    yield ext, unit, submission
            except LudicrousConditions as e:
                logger.warning(_("%s could not discover submissions") + ': %s. %s', ext.name, e.error, e.suggestion)

    def fnmatch_units(self, patterns, units):
        return [
            unit
            for unit in units
            if any(fnmatch(unit.task, pattern) for pattern in patterns)
        ]

    def section_apis(self, config):
        """ Return section, API class pair.
        """
        for __, section in config.items():
            if section.name == 'DEFAULT':
                continue
            if 'api' in section:
                ident = section['api']
                if ident in API_CLASSES:
                    api = API_CLASSES[ident].from_config(section)
                    yield section, api
            else:
                logger.debug("Unrecognized section %s.", section)

    def section_exts(self, config):
        """ Returns section, Ext class pair.
        """
        for section, api in self.section_apis(config):
            name = section.get('name', section.name)
            assert name, "Unnamed sections are for jerks"
            abbr = section.get('abbr', name[0].upper())
            yield section, Ext(api=api, name=name, abbr=abbr)
