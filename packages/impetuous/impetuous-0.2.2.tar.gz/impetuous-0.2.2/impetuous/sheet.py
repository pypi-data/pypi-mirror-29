from fnmatch import fnmatch
from pathlib import Path
import datetime
import functools
import itertools
import logging
import math
import os
import random
import re
import time

import dateutil.parser
import yaml
try:
    from yaml import (
        CLoader as yaml_Loader,
        CDumper as yaml_Dumper,
    )
except ImportError:
    from yaml import (
        Loader as yaml_Loader,
        Dumper as yaml_Dumper,
    )


logger = logging.getLogger(__name__)

utctz = datetime.timezone.utc
localtz = dateutil.tz.tzlocal()

DEFAULT_SHEET_PATH = Path.home() / '.local' / 'share' / 'impetuous'
ENV_SHEET_PATH = os.environ.get('IM_SHEET_DIR', DEFAULT_SHEET_PATH)


def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


class WhenTime(object):

    class UnitSeek(object):

        class StartEdge:
            pass

        class EndEdge:
            pass

        def __init__(self, count, edge):
            self.count = count
            self.edge = edge

    def __init__(self, initial, seek=None, delta=None):
        assert initial.tzinfo is not None
        self.initial = initial
        self.seek = seek
        self.delta = delta

    def absolute_datetime(self, units):
        """
        Return an absolute date and time, possibly relative to some given
        units if this WhenType specifies a delta (such as relative to a unit's
        start/end time).
        """
        value = self.initial
        if self.seek is not None:
            steps = []
            for unit in units:
                if self.seek.edge is self.seek.StartEdge:
                    time = unit.start
                else:
                    time = unit.end
                if time is None:
                    raise ValueError(_("Refusing seek past null time."))
                elif time < value:
                    steps.append(time)
                else:
                    break
            try:
                value = steps[-self.seek.count]
            except IndexError:
                raise UnitNotFoundError(_("No unit matching seek."))
        if self.delta is not None:
            value += self.delta
        return value


class WhenArgType(object):
    """
    It's important to use utcnow and the local timezone as attributes on this
    guy instead of just localtimenow because otherwise, time zones will fuck
    you in weird ways.

    Trust me. UTC is the only sane time zone. Use it as much as possible.
    """

    when_format_re = re.compile(
        # Fixed initial
        r'((\.|now)|(?:(\d{1,2}):(\d{1,2}):?(\d{1,2})?))?'
        # Seek
        r'(([[\]])(\d*))?'
        # Relative offset
        r'(([+-])(\d+h)?(\d+m)?(\d+s)?)?'
        r'$'
    )

    def __init__(self, utcnow=utcnow, localtz=localtz):
        self.utcnow = utcnow
        self.localtz = localtz

    def __repr__(self):
        """ For formatting nicely when displayed in an argument parsing message.
        """
        return 'WhenArgType'

    def __call__(self, text):
        """
        Returns a WhenTime which can be used to produce an absolute time given
        the context of a collection of units.
        """
        if text == 'now':
            return WhenTime(self.utcnow())

        match = self.when_format_re.match(text)
        if match is not None:
            (initial, initial_dot, initial_hour, initial_minute, initial_second,
             seek, seek_edge, seek_count,
             delta, delta_sign, delta_hours, delta_minutes, delta_seconds
             ) = match.groups()

            # Set initial
            if initial is None or initial_dot:
                initial = self.utcnow()
            else:
                time = datetime.time(hour=int(initial_hour),
                                     minute=int(initial_minute),
                                     second=0 if initial_second is None else int(initial_second[0:]))
                now = self.utcnow()
                today = now.astimezone(self.localtz).date()
                initial = datetime.datetime.combine(today, time).replace(tzinfo=self.localtz)

            # Set seek
            if seek is not None:
                if seek_edge == '[':
                    seek_edge = WhenTime.UnitSeek.StartEdge
                else:
                    seek_edge = WhenTime.UnitSeek.EndEdge
                seek = WhenTime.UnitSeek(edge=seek_edge,
                                         count=int(seek_count) if seek_count else 1)

            # Finally make relative/delta time adjustment
            if delta is not None:
                delta = datetime.timedelta(
                    hours=0 if delta_hours is None else int(delta_hours[:-1]),
                    minutes=0 if delta_minutes is None else int(delta_minutes[:-1]),
                    seconds=0 if delta_seconds is None else int(delta_seconds[:-1])
                )
                if delta_sign == '-':
                    delta = -delta

            return WhenTime(initial=initial, seek=seek, delta=delta)
        else:
            raise ValueError(_("Bad format '{}'.").format(text[0:]))


class UnitNotFoundError(RuntimeError):
    pass


class SheetNotFoundError(RuntimeError):
    pass


class LinkNotFoundError(RuntimeError):
    pass


class ValidationError(Exception):

    def __init__(self, message, params=None):
        if params is None:
            params = {}
            super().__init__(message)
        else:
            super().__init__(message.format(**params))
        self.message = message
        self.params = params


def format_comments(comments):
    if len(comments) == 1:
        return comments[0]
    else:
        return '\n'.join('- %s' % comment for comment in comments)


class Unit(object):

    def __init__(self, start, task, end=None, covert=False, post_results=None, comments=None):
        assert start.tzinfo is not None
        if end is not None:
            assert end.tzinfo is not None
        self.start = start
        self.task = task
        self.end = end
        self.covert = covert
        self.post_results = post_results or {}
        self.comments = [] if comments is None else comments

    def __contains__(self, other):
        return (
                (other.end is not None and other.start <= self.start < other.end)
                or (self.end is not None and self.start <= other.start < self.end)
                )

    def validate(self):
        if self.end is not None and self.end < self.start:
            raise ValidationError(_("Unit cannot end at {} before it begins at {}.").format(self.end, self.start))

    @property
    def duration(self):
        if self.end is None:
            end = utcnow()
        else:
            end = self.end
        return end - self.start

    @property
    def duration_in_minutes(self):
        """ Return duration in minutes as integer. Rounds randomly. :)
        """
        minutes_spent = self.duration.total_seconds() / 60
        if minutes_spent % 1 <= random.random():
            return math.floor(minutes_spent)
        else:
            return math.ceil(minutes_spent)

    @property
    def full_comment(self):
        return format_comments(self.comments)

    @classmethod
    def yaml_representer(cls, dumper, unit):
        as_dict = {
            'start': unit.start.astimezone(localtz),
            'task': unit.task,
        }
        if unit.end is not None:
            as_dict['end'] = unit.end.astimezone(localtz)
        if unit.covert:
            as_dict['covert'] = True
        if unit.post_results:
            as_dict['post_results'] = unit.post_results
        if unit.comments:
            as_dict['comments'] = unit.comments
        return dumper.represent_mapping(u'!unit', as_dict)

    @classmethod
    def yaml_constructor(cls, loader, node):
        return cls(**loader.construct_mapping(node, deep=True))


class Sheet(object):

    def __init__(self, name=None, links=None, units=None):
        self.name = name
        self.links = links or {}
        self.units = units or []

    def new_unit(self, *args, **kwargs):
        new_unit = Unit(*args, **kwargs)
        self.units.append(new_unit)
        self.units.sort(key=lambda unit: unit.start)
        return new_unit

    def validate(self):
        for i, unit in enumerate(self.units):
            unit.validate()
            for other in self.units[i+1:]:
                if other in unit:
                    raise ValidationError(_("Unit {a} overlaps with {b}."), dict(a=unit, b=other))

    @property
    def current_unit(self):
        """ Return a unit with no end; raises UnitNotFoundError if impossible.
        """
        try:
            return next(unit for unit in reversed(self.units) if unit.end is None)
        except StopIteration:
            raise UnitNotFoundError(_("No units with no end found."))

    def get_last_ended_unit(self):
        units = filter(lambda unit: unit.end is not None, self.units)
        if units:
            return sorted(units, key=lambda unit: unit.end, reverse=True)[0]

    @classmethod
    def yaml_representer(cls, dumper, sheet):
        return dumper.represent_mapping(u'!sheet', {
            'links': sheet.links,
            'units': sheet.units,
        })

    @classmethod
    def yaml_constructor(cls, loader, node):
        return cls(**loader.construct_mapping(node, deep=True))


class SheetDirectory(object):
    """ TODO refactor this into some sort of sheet(/unit) manager thingy
    """

    def __init__(self, path):
        self.path = path
        # Will this even work? This is bananas...
        class SheetDirectory_yaml_Dumper(yaml_Dumper):
            pass
        class SheetDirectory_yaml_Loader(yaml_Loader):
            pass
        self._yaml_dumper = SheetDirectory_yaml_Dumper
        self._yaml_loader = SheetDirectory_yaml_Loader
        self._yaml_dumper.add_representer(Unit, Unit.yaml_representer)
        self._yaml_dumper.add_representer(Sheet, Sheet.yaml_representer)
        self._yaml_loader.add_constructor(u'!unit', Unit.yaml_constructor)
        self._yaml_loader.add_constructor(u'!sheet', Sheet.yaml_constructor)
        self._yaml_loader.add_constructor(u'tag:yaml.org,2002:timestamp', timestamp_constructor)

    def new(self, name):
        return Sheet(name=name)

    def save(self, sheet):
        if not sheet.name:
            raise ValueError(_("Sheet is unnamed, should this be a ValidationError?"))
        try:
            self.path.mkdir(parents=True)
        except FileExistsError:
            pass
        sheet_path = self.path / sheet.name
        tmp_sheet_path = self.path / (sheet.name + '~')

        logger.debug("Writing to %s", tmp_sheet_path)
        with tmp_sheet_path.open('w') as file:
            yaml.dump(sheet, file, indent=4, default_flow_style=False, Dumper=self._yaml_dumper)

        logger.debug("Moving to %s", sheet_path)
        tmp_sheet_path.rename(sheet_path)

    def load_file(self, file):
        sheet = yaml.load(file, Loader=self._yaml_loader)
        if sheet is None:
            raise SheetNotFoundError(_("Sheet exists on filesystem but is empty."))
        sheet.name = Path(file.name).name
        return sheet

    def load(self, name):
        sheet_path = self.path / name
        try:
            with sheet_path.open('r') as file:
                return self.load_file(file)
        except FileNotFoundError as e:
            raise SheetNotFoundError(e)

    def load_or_create(self, name):
        try:
            return self.load(name)
        except SheetNotFoundError:
            return self.new(name)


# http://stackoverflow.com/a/13295663
def timestamp_constructor(loader, node):
    return dateutil.parser.parse(node.value)
