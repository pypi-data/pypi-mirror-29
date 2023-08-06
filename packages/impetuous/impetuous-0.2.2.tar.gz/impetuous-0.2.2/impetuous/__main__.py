#!/usr/bin/env python3

import asyncio
import argparse
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import timedelta
import logging
import gettext
import pdb

import colorama as ca

from impetuous.sheet import (
    SheetNotFoundError,
    UnitNotFoundError,
    WhenArgType,
    utcnow,
    localtz,
)
from impetuous.cli import (
    ImpetuousCli,
    CURRENT_SHEET_FMT,
    FUNCTION_DEST,
    im_a,
    im_comment,
    im_config_edit,
    im_done,
    im_edit,
    im_encode,
    im_decode,
    im_log,
    im_post,
    im_rename,
    im_starting,
    im_summary,
)


logger = logging.getLogger('impetuous')


def main():
    # Initialize colorama stuff
    ca.init()

    # Localization? Maybe?
    import os.path
    ld = os.path.join(os.path.dirname(__file__), '..', 'locale')
    gettext.install('impetuous', ld)

    # Some arguments we want to know earlier, but we don't want
    # parse_known_args to throw up if it sees '-h', so we create a parser with
    # add_help=False, then add help later on after parsing early arguments.
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, add_help=False)
    parser.add_argument('-l', '--log',
                        help='Logging level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='WARNING')
    parser.add_argument('-y', '--yesterday', action='count', default=0)
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args, _ = parser.parse_known_args()

    logging.basicConfig(level=getattr(logging, args.log))
    utcnow_ish = lambda: utcnow() - timedelta(days=args.yesterday)
    current_sheet = CURRENT_SHEET_FMT.format(local_time=utcnow_ish().astimezone(localtz))
    impetuous = ImpetuousCli(current_sheet)

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='action')
    subparser.required = True
    subparser.dest = FUNCTION_DEST

    log_help = '''Show a list things done, startings, endings, and durations
    for the current sheet.'''
    log_args = subparser.add_parser('log', help=log_help, aliases=['l'], formatter_class=ArgumentDefaultsHelpFormatter)
    log_args.add_argument('--reverse', '-r', action='store_true', default=False)
    log_args.add_argument('--verbose', '-v', action='store_true', default=False)
    log_args.set_defaults(action=im_log)

    summary_help = '''Show a summary of total time spent on things in the
    current sheet.'''
    summary_args = subparser.add_parser('summary', help=summary_help, aliases=['ll'], formatter_class=ArgumentDefaultsHelpFormatter)
    summary_args.set_defaults(action=im_summary)

    start_help = '''Mark the start of doing a new thing, stopping any current
    things if applicable.'''
    start_args = subparser.add_parser('starting', help=start_help, aliases=['s', 'start'], formatter_class=ArgumentDefaultsHelpFormatter)
    start_args.add_argument('what', type=str)
    start_args.add_argument('when', type=WhenArgType(utcnow=utcnow_ish), nargs='?', default='now', help='Start of period')
    start_args.add_argument('--covert', action='store_true', default=False, help='Covert entries do not show up in summaries (they do show up in the log) and are never posted.')
    start_args.add_argument('--comment', '-c', type=str, nargs='?', help='')
    start_args.set_defaults(action=im_starting)

    comment_help = '''Add a comment to a thing being done.'''
    comment_args = subparser.add_parser('comment', help=comment_help, aliases=['c'], formatter_class=ArgumentDefaultsHelpFormatter)
    comment_args.add_argument('words', type=str, nargs='+')
    comment_args.set_defaults(action=im_comment)

    done_help = '''Mark the ending of the current thing being done.'''
    done_args = subparser.add_parser('done', help=done_help, aliases=['d'], formatter_class=ArgumentDefaultsHelpFormatter)
    done_args.add_argument('when', type=WhenArgType(utcnow=utcnow_ish), nargs='?', default='now')
    done_args.set_defaults(action=im_done)

    rename_help = '''Renames every thing done in this sheet called <old> to
    <new>, <old> defaults to what is being done currently.'''
    rename_args = subparser.add_parser('rename', help=rename_help, aliases=['r'], formatter_class=ArgumentDefaultsHelpFormatter)
    rename_args.add_argument('old', nargs='?', default=None)
    rename_args.add_argument('new')
    #rename_args.add_argument('-a', '--all', help='Rename all units that match')
    rename_args.set_defaults(action=im_rename)

    edit_help = '''Opens the current sheet in EDITOR.'''
    edit_args = subparser.add_parser('edit', help=edit_help)
    edit_args.set_defaults(action=im_edit)

    config_help = '''Opens the config in EDITOR.'''
    config_args = subparser.add_parser('config-edit', help=config_help)
    config_args.set_defaults(action=im_config_edit)

    post_help = '''Submits worklogs to JIRA and Freshdesk.'''
    post_args = subparser.add_parser('post', help=post_help, formatter_class=ArgumentDefaultsHelpFormatter)
    post_args.add_argument('units', type=str, nargs='*', help='Submit all vaild units with names match the glob.', default='*')
    post_args.add_argument('-n', '--dry_run', action='store_true', default=False, help='Do not actually send submissions, just talk about them.')
    post_args.set_defaults(action=im_post)

    encode_help = '''Encodes passwords/secrets in the config using a given
    codec. The config parser is very rude and will does not preserve comments
    anything in your config file when this modifies it.'''
    encode_args = subparser.add_parser('encode', help=encode_help, formatter_class=ArgumentDefaultsHelpFormatter)
    encode_args.add_argument('codec', choices=['base64', 'bz2', 'hex', 'quotedprintable', 'uu', 'zlib'])
    encode_args.set_defaults(action=im_encode)

    decode_help = '''Decodes passwords in the config using a given codec. The
    config parser is very rude and will does not preserve comments anything in
    your config file when this modifies it.'''
    decode_args = subparser.add_parser('decode', help=decode_help, formatter_class=ArgumentDefaultsHelpFormatter)
    decode_args.set_defaults(action=im_decode)

    a_help = '''What are you?.'''
    a_args = subparser.add_parser('a', aliases=['an'], help=a_help, formatter_class=ArgumentDefaultsHelpFormatter)
    a_args.add_argument('?', type=str, nargs='+')
    a_args.set_defaults(action=im_a)

    try:
        args = parser.parse_args()
    except KeyboardInterrupt:
        logger.info("Bye!")
    except SystemExit:
        raise
    except Exception as e:
        if args.debug:
            logger.exception(e)
            pdb.post_mortem()
        raise
    action = args.action

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(action(impetuous, args))
    except (ValueError, SheetNotFoundError, UnitNotFoundError) as e:
        logger.error(e)
    except KeyboardInterrupt:
        logger.info("Bye!")
    except SystemExit:
        raise
    except Exception as e:
        if args.debug:
            logger.exception(e)
            pdb.post_mortem()
        raise
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == '__main__':
    main()
