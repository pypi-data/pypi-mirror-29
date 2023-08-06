"""
Impetuous and actions invoked from argument parser.
"""

from random import random, shuffle
import asyncio
import codecs
import contextlib
import datetime
import itertools
import logging
import math
import os
import subprocess

import colorama as ca
import attr

from impetuous.config import (
    CONFIG_INI_PATH,
    CONFIG_DIR,
    write_config,
    CodedValue
)
from impetuous.sheet import (
    SheetDirectory,
    Unit,
    SheetNotFoundError,
    UnitNotFoundError,
    ValidationError,
    DEFAULT_SHEET_PATH,
    utcnow,
    localtz,
)
from impetuous.ext import LudicrousConditions, SubmissionStatus
from impetuous.im import Impetuous


CURRENT_SHEET_FMT = os.environ.get('IM_SHEET_FMT', '{local_time:%Y-%m-%d}')
FUNCTION_DEST = 'the thing it is that you are trying to do'

logger = logging.getLogger(__name__)


def maybe_elide(string, max_length):
    r"""
    >>> maybe_elide('Hello world', 4)
    'H...'
    >>> maybe_elide('Hello world', 5)
    'H...d'
    >>> maybe_elide('Hello world', 9)
    'Hel...rld'
    >>> maybe_elide('Hello world', 10)
    'Hell...rld'
    >>> maybe_elide('Hello world', 11)
    'Hello world'
    >>> maybe_elide('Spam and eggs!', 9)
    'Spa...gs!'
    >>> maybe_elide('Spam and eggs!', 10)
    'Spam...gs!'
    >>> maybe_elide('We have phasers, I vote we blast \'em!   -- Bailey, "The Corbomite Maneuver", stardate 1514.2', 29)
    'We have phase...ardate 1514.2'

    """
    assert max_length > 3
    if len(string) > max_length:
        chunklen = (max_length - 3) // 2
        return "{}...{}".format(string[:chunklen + 1],
                                '' if chunklen == 0 else string[-chunklen:])
    else:
        return string


def sanitize(string):
    r"""
    Sanitize for one-line printing?

    >>> sanitize('foo\nbar\tbaz')
    'foo bar baz'

    """
    return string.replace('\t', ' ').replace('\n', ' ')


def get_terminal_width():
    """
    Return the terminal width as an integer or None if we can't figure it out.
    """
    try:
        stty = subprocess.check_output(['stty', 'size'])
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    else:
        try:
            return int(stty.strip().split(b' ')[1])
        except (ValueError, IndexError):
            pass
    try:
        tput = subprocess.check_output(['tput', 'cols'])
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    else:
        try:
            return int(tput.strip())
        except ValueError:
            pass
    try:
        env = subprocess.check_output('echo -n $COLUMNS', shell=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    else:
        try:
            return int(env)
        except ValueError:
            pass


def open_in_editor(path):
    if not 'EDITOR' in os.environ:
        logger.warning(_("EDITOR not set, using `ed`."))
        editor = 'ed'
    else:
        editor = '$EDITOR'
    subprocess.check_call(editor + ' ' + str(path), shell=True)


class ImpetuousCli(Impetuous):
    """
    Mostly stuff about displaying to the CLI...

    TODO compose not inherit
    """

    def __init__(self, current_sheet_name):
        super().__init__()
        self.current_sheet_name = current_sheet_name
        self.dir = SheetDirectory(DEFAULT_SHEET_PATH)

    def _format_validation_err(self, err):  # TODO this should probably be in ImpetuousCli ...
        params = err.params.copy()
        for key, value in params.items():
            if isinstance(value, Unit):
                unit = value
                params[key] = "".join((ca.Style.BRIGHT, unit.task, ca.Fore.BLUE, '@', ca.Fore.GREEN, self.format_datetime(unit.start), ca.Style.RESET_ALL))
        return ValidationError(message=err.message, params=params)

    def validate_sheet(self, sheet):
        try:
            sheet.validate()
        except ValidationError as err:
            logger.error(self._format_validation_err(err))
            raise SystemExit(1)

    def save_sheet(self, sheet):
        try:
            return self.dir.save(sheet)
        except OSError as err:
            logger.error(str(err))
            raise SystemExit(1)

    def log(self, sheet, *, verbose=False, reverse=False):
        units = sorted(sheet.units, key=lambda unit: unit.start, reverse=reverse)
        while units:
            unit = units.pop(0)
            self.print_unit(unit, verbose=verbose)
            if units:
                next_unit = units[0]
                if reverse:
                    gap = unit.start - (next_unit.end or utcnow())
                else:
                    gap = next_unit.start - (unit.end or utcnow())
                if gap > datetime.timedelta(seconds=1):
                    print(ca.Fore.MAGENTA, '(', self.format_timedelta(gap), ')', ca.Style.RESET_ALL, sep='')

    def print_unit_submissions(self, unit, verbose=False):
        config = self.get_config_or_none()
        if config is not None:
            for module, unit, submission in self.get_unit_submissions(unit):
                print(' ', end='')
                self.print_unit_submission(module, unit, submission, verbose=verbose)

    def print_unit_submission(self, module, unit, submission, *, verbose):
        status = submission.status(unit)
        if verbose:
            print(module.name, end='')
            print('[', end='')
        else:
            print(module.abbr, end='')
        if status is SubmissionStatus.invalid:
            print(ca.Style.BRIGHT, ca.Fore.RED, '!', ca.Style.RESET_ALL, sep='', end='')
        elif status is SubmissionStatus.unsubmitted:
            print(ca.Style.BRIGHT, '*', ca.Style.RESET_ALL, sep='', end='')
        else:
            pass
        if verbose:
            print(submission.label, end=']')

    def print_unit(self, unit, verbose=True):
        self.print_unit_start(unit, end=' ')
        self.print_unit_duration(unit, end=' ')
        self.print_unit_end(unit, end=' ')
        self.print_unit_task(unit, end='')
        if verbose:
            self.print_unit_submissions(unit, verbose=verbose)
            print()
            if unit.comments:
                for comment in unit.comments:
                    print(' - %s' % comment)
        else:
            if unit.comments:
                # start
                room = get_terminal_width() - 28 - len(unit.task)
                room -= 2  # surrounding braces
                room -= 2 * (len(unit.comments) - 1)  # '; ' join
                comment_length = room // len(unit.comments)
                comments = (maybe_elide(sanitize(comment), comment_length)
                            for comment in unit.comments)
                print(' (%s)' % '; '.join(comments), end='')
            self.print_unit_submissions(unit, verbose=verbose)
            print()

    def print_unit_task(self, unit, **kwargs):
        if unit.covert:
            print('(', unit.task, ')', sep='', **kwargs)
        else:
            print(ca.Style.BRIGHT, unit.task, ca.Style.RESET_ALL, sep='', **kwargs)

    def print_unit_start(self, unit, **kwargs):
        print(ca.Style.BRIGHT, ca.Fore.GREEN, self.format_datetime(unit.start), ca.Style.RESET_ALL, sep='', **kwargs)

    def print_unit_end(self, unit, **kwargs):
        print(ca.Fore.GREEN, self.format_datetime(unit.end), ca.Fore.RESET, sep='', **kwargs)

    def format_datetime(self, dt):
        if dt is None:
            return '--:--:--'
        else:
            dt = dt.astimezone(localtz)
            is_today = dt.date() == utcnow().astimezone(localtz).date()
            if is_today:
                return dt.time().strftime('%H:%M:%S')
            else:
                return dt.strftime('%Y-%m-%d %H:%M:%S')

    def print_unit_duration(self, unit, **kwargs):
        self.print_timedelta(unit.duration, **kwargs)

    def print_timedelta(self, delta, **kwargs):
        print(ca.Fore.BLUE, ca.Style.BRIGHT, self.format_timedelta(delta), ca.Style.RESET_ALL, ca.Fore.RESET, sep='', **kwargs)

    def format_timedelta(self, delta):
        seconds = int(delta.total_seconds())
        if seconds < 0:
            negate = True
            seconds = abs(seconds)
        else:
            negate = False
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return '{}{:}:{:02}:{:02}'.format('-' if negate else '', hours, minutes, seconds)


async def im_summary(impetuous, args):
    sheet = impetuous.dir.load(impetuous.current_sheet_name)
    keyfnc = lambda unit: unit.task
    summary_units = sorted((unit for unit in sheet.units if not unit.covert), key=keyfnc)
    for task, units in itertools.groupby(summary_units, keyfnc):
        total = sum((unit.duration for unit in units), datetime.timedelta(0))
        # This is awkward
        start = utcnow()
        unit = Unit(task=task, start=start, end=start+total)
        impetuous.print_unit_duration(unit, end=' ')
        impetuous.print_unit_task(unit)
    grand_total = sum((unit.duration for unit in summary_units), datetime.timedelta(0))
    start = utcnow()
    impetuous.print_unit_duration(Unit(task='', start=start, end=start+grand_total))


async def im_a(impetuous, args):
    what = ' '.join(getattr(args, '?'))
    article = getattr(args, FUNCTION_DEST)
    colors = [ca.Fore.GREEN, ca.Fore.BLUE, ca.Fore.MAGENTA]
    shuffle(colors)
    c = itertools.cycle(colors)
    color = lambda: next(c)
    if article == 'a' and what.lower() == 'real human being':
        response = "...", "and", "a", "real", "hero"
        punctuation = "!"
    else:
        response = "You", "are", article, *what.split()
        punctuation = "."
    for token in response[:-1]:
        print(token, color(), sep=" ", end="")
    print(response[-1], ca.Style.RESET_ALL, punctuation, ca.Style.RESET_ALL, sep="", end="\n")


async def im_log(impetuous, args):
    sheet = impetuous.dir.load(impetuous.current_sheet_name)
    impetuous.log(sheet, verbose=args.verbose, reverse=args.reverse)


async def im_starting(impetuous, args):
    start_task = args.what
    if start_task == '-':
        sheet = impetuous.dir.load(impetuous.current_sheet_name)
        unit = sheet.get_last_ended_unit()
        if unit is None:
            raise UnitNotFoundError()
        start_task = unit.task

    try:
        await im_done(impetuous, args)
    except (SheetNotFoundError, UnitNotFoundError):
        pass

    sheet = impetuous.dir.load_or_create(impetuous.current_sheet_name)
    start_when = args.when.absolute_datetime(sheet.units)
    unit = sheet.new_unit(start=start_when, task=start_task, covert=args.covert, comments=args.comment)
    impetuous.validate_sheet(sheet)
    impetuous.save_sheet(sheet)
    impetuous.print_unit(unit)


async def im_comment(impetuous, args):
    sheet = impetuous.dir.load(impetuous.current_sheet_name)
    unit = sheet.current_unit
    if any(submission.status(unit) is SubmissionStatus.submitted
           for _, _, submission in impetuous.get_unit_submissions(unit)):
        logger.warning(_("Modifying a unit with posted submissions."))
    unit.comments.append(' '.join(args.words))
    impetuous.validate_sheet(sheet)
    impetuous.dir.save(sheet)
    impetuous.print_unit(unit, verbose=True)


async def im_done(impetuous, args):
    sheet = impetuous.dir.load(impetuous.current_sheet_name)
    unit = sheet.current_unit
    if unit.end is None:
        unit.end = args.when.absolute_datetime(sheet.units)
        impetuous.validate_sheet(sheet)
        impetuous.dir.save(sheet)
        impetuous.print_unit(unit)
    else:
        raise UnitNotFoundError(_("The last unit is not in progress."))


async def im_edit(impetuous, args):
    open_in_editor(impetuous.dir.path / impetuous.current_sheet_name)


async def im_config_edit(impetuous, args):
    filepath = CONFIG_INI_PATH
    try:
        filepath.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    else:
        logger.info(_("%s created."), filepath.parent)
    open_in_editor(filepath)


async def im_rename(impetuous, args):
    sheet = impetuous.dir.load(impetuous.current_sheet_name)
    if not sheet.units:
        raise UnitNotFoundError(_("The current sheet is empty."))
    else:
        if args.old is None:
            old_task = sheet.units[-1].task
        else:
            old_task = args.old
        changed = False
        for unit in sheet.units:
            if unit.task == old_task:
                print(_("Renaming "), end="")
                impetuous.print_unit_start(unit, end=" ")
                impetuous.print_unit_task(unit, end=" ")
                print(_("to "), end="")
                unit.task = args.new
                impetuous.print_unit_task(unit)
                impetuous.print_unit(unit)
                changed = True
        if not changed:
            print(_("Nothing to do."))
        else:
            impetuous.validate_sheet(sheet)
            impetuous.dir.save(sheet)


class FakeSubmissionResult(object):

    def __init__(self, submission):
        pass


async def im_post(impetuous, args):
    config = impetuous.get_config_or_quit()
    sheet = impetuous.dir.load(impetuous.current_sheet_name)
    units = impetuous.fnmatch_units(args.units, sheet.units)
    if not units:
        logger.error(_("No matching units!"))
        raise SystemExit(1)

    agents = {}
    tasks = {}
    iter_subs = impetuous.get_unit_submissions(*units)
    try:
        for ext, unit, submission in iter_subs:
            if submission.status(unit) is not SubmissionStatus.unsubmitted:
                continue
            if ext in agents:
                agent = agents[ext]
            else:
                agent = agents[ext] = await ext.api.agent(impetuous)
            job = PostJob(impetuous, ext, agent, unit, submission, args.dry_run)
            task = asyncio.get_event_loop().create_task(job.post())
            tasks[task] = job

        logger.debug("Posting jobs: %r", tasks)
        pending = tasks.keys()
        while pending:
            logger.debug(_("im_post waiting for: %r."), pending)
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                result = task.result()  # Rethrow exceptions
                job = tasks[task]
                if result is None:  # Assume an error in PostJob???
                    print("The Lord looked with favor on Abel and his offering, but on Cain and his offering (at ", end="")
                    impetuous.print_unit_start(job.unit, end=" Cain did ")
                    impetuous.print_unit_duration(job.unit, end=" of ")
                    impetuous.print_unit_submission(job.ext, job.unit, job.submission, verbose=True)
                    print(") he did not look with favor. So Cain was very angry, and his face was downcast.")
                else:
                    print("And so it was written; at ", end="")
                    impetuous.print_unit_start(job.unit, end=" you did ")
                    impetuous.print_unit_duration(job.unit, end=" of ")
                    impetuous.print_unit_submission(job.ext, job.unit, job.submission, verbose=True)
                    print()
            if not args.dry_run:
                # We don't validate here because who cares
                impetuous.dir.save(sheet)
    finally:
        logger.debug(_("Cleaning up posting context."))
        for task in tasks.keys():
            if not task.done():
                logger.debug(_("Trying to tidy up incomplete %s."), task)
                task.cancel()
        if tasks:
            await asyncio.wait(tasks.keys())
        for agent in agents.values():
            await agent.close()


@attr.s(frozen=True, hash=False)
class PostJob(object):

    impetuous = attr.ib()
    ext = attr.ib()
    agent = attr.ib()
    unit = attr.ib()
    submission = attr.ib()
    dry_run = attr.ib()

    async def post(self):
        if self.dry_run:
            await asyncio.sleep(random() % 0.5)
            result = FakeSubmissionResult(self.submission)
        else:
            logger.debug(_("Submitting %r..."), self.submission)
            try:
                result = await self.agent.submit(self.submission)
            except LudicrousConditions as e:
                logger.error(_("%s failed to submit %r") + ': %s. %s',
                             type(self.ext).__name__, self.submission, e.error, e.suggestion)
                return
        logger.debug(_("Submitted %r with result %r."), self.submission, result)
        self.submission.update_submitted_unit(self.unit, result)
        return result


def try_encode_field(section, field, codec):
    key = field.name
    try:
        current = CodedValue.from_config(section, key)
    except KeyError as err:
        logger.err(_("Something didn't work: %s"), err)
        raise SystemExit(1)
    else:
        logger.warning(_("Encoding `%s.%s%s` with %s."), section.name, key, current.config_key_suffix, codec)
        encoded = current.encode(codec)
        section[key + encoded.config_key_suffix] = encoded.encoded
        del section[key + current.config_key_suffix]


def try_decode_field(section, field):
    key = field.name
    try:
        current = CodedValue.from_config(section, key)
    except KeyError as err:
        logger.err(_("Something didn't work: %s"), err)
        raise SystemExit(1)
    else:
        if current.is_encoded:
            logger.warning(_("Decoding `%s.%s%s`."), section.name, key, current.config_key_suffix)
            decoded = current.decode()
            section[key + decoded.config_key_suffix] = decoded.encoded
            del section[key + current.config_key_suffix]
        else:
            logger.warning(_("`%s.%s%s` not encoded; doing nothing."), section.name, key, current.config_key_suffix)


async def im_encode(im, args):
    config = im.get_config_or_quit()
    for section, api in im.section_apis(config):
        for field in api.coded_fields():
            try_encode_field(section, field, args.codec)
    write_config(config)


async def im_decode(im, args):
    config = im.get_config_or_quit()
    for section, api in im.section_apis(config):
        for field in api.coded_fields():
            try_decode_field(section, field)
    write_config(config)
