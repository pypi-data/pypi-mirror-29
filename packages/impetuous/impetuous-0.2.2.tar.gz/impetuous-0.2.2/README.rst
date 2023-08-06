Impetuous
=========

.. image:: https://img.shields.io/badge/downloads-743M%2Fday-brightgreen.svg
.. image:: https://img.shields.io/badge/coverage-no-lightgrey.svg
.. image:: https://img.shields.io/badge/build-disappointed-blue.svg
.. image:: https://img.shields.io/badge/node.js-webscale-orange.svg
.. image:: https://img.shields.io/badge/available%20on-itunes-9377db.svg
.. image:: https://img.shields.io/badge/uptime-since%20lunch-78bdf2.svg
.. image:: https://img.shields.io/badge/kony-2012-ff69b4.svg

This is some time/task tracking software. 🐑

It can talk (barely) to/at JIRA.

Requirements
------------

python 3.4 (or 3.5 just to be safe)

Installation
------------

Clone the source code and install with :code:`python3 -m pip install --user -e .[jira,freshdesk]`. If you want. :sup:`You don't have to.` :sub:`I'm not the police.`

CLI Usage
---------

Sheets live in the directory :code:`~/.config/impetuous/sheets`. They are in the YAML file format.

The "current sheet" is some file in the sheet directory. The name of the sheet that is considered the "current" one follows the format in the environment variable :code:`IM_SHEET_FMT` and defaults to :code:`{local_time:%Y-%m-%d}`. The format string is formatted with the local time using python's :code:`str.format()` function such that, by default, impetuous will use a different sheet each day.

A number of commands take a :code:`when` argument. This has a number of acceptable formats. I can't explain it since it's over-engineered and stupid. Here are some examples:

- :code:`14:15` - 2:15 P.M.
- :code:`.+1h5s` - One hour and five seconds after now.
- :code:`.-10m` - Ten minutes before now.
- :code:`]+90s` - Ninety seconds after the end of the last/current task.
- :code:`[+1h5s` - One hour and five seconds after the beginning of the last/current task.

Examples
^^^^^^^^

Here's a thing:

.. image:: https://asciinema.org/a/dxbieo504w9obhetfvzvqwtix.png?theme=tango
    :width: 460px
    :alt: Usage Demo
    :target: https://asciinema.org/a/dxbieo504w9obhetfvzvqwtix?theme=tango&autoplay=1

It took me three hours to record that without typos ...  (:code:`im start therapy`)

Encoding
^^^^^^^^

You can use `im encode` to get impetuous to encode your passwords in the configuration file. Then it decodes them when it uses them. It supports a few different encodings. You can encode it multiple times. I don't know why you want to use this. But it's there now.

Limitations
-----------

Who knows? If you find one, make a feature report.

Configuration and JIRA and Freskdesk
------------------------------------

Edit the configuration by running :code:`im config-edit`, which just opens the configuration file in :code:`~/.config/impetuous/config.ini` in :code:`EDITOR`. This is an example :code:`config.ini`::

    [jira]
    api = jira
    server = https://funkymonkey.atlassian.net
    basic_auth = admin:hunter2
    pattern = ((?:FOO-\d+)|(?:BAR-\d+))

    [freshdesk]
    api = freshdesk
    server = https://funkymonkey.freshdesk.com
    api_key = xxxxxxxxxxxxxxxxxxxx
    pattern = freskdesk (\d+)
    name = sheepdesk
    abbr = 🐑

Each section defines an external service for logging time against. The
:code:`api` determines how we can talk to it. You can add multiple sections and
call them whatever you want.

By default, the name and abbreviated name are taken from the section name, but
you can set them as shown in the "freshdesk" section above.

Tests
-----

Oh man, I don't know. Just run :code:`python3 -m pytest` and hope for the best I suppose.

Internationalization / Localization
-----------------------------------

Maybe?

#. :code:`python3 setup.py extract_messages`
#. :code:`python3 setup.py update_catalog -l fr`
#. Modify the translation file ending in :code:`.po` ... if you want
#. :code:`python3 setup.py compile_catalog`
#. Run with :code:`LANGUAGE=fr`

You actually only need to do step 4 and 5 to run the program with localization
if you don't want to make modifications.
