diceware
========

Passphrases to remember...

|bdg-build|  | `documentation <https://diceware.readthedocs.io/>`_ | `sources <https://github.com/ulif/diceware>`_ | `issues <https://github.com/ulif/diceware/issues>`_

.. |bdg-build| image:: https://travis-ci.org/ulif/diceware.png?branch=master
    :target: https://travis-ci.org/ulif/diceware
    :alt: Build Status

.. |bdg-last-release|  image:: https://img.shields.io/pypi/v/diceware.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: Latest Release

.. |bdg-versions| image:: https://img.shields.io/pypi/pyversions/diceware.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: Supported Python Versions

.. |bdg-license| image:: https://img.shields.io/pypi/l/diceware.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: License

.. |doc-status| image:: https://readthedocs.io/projects/diceware/badge/?version=latest
     :target: https://diceware.readthedocs.io/en/latest/
     :alt: Documentation Status

`diceware` is a passphrase generator following the proposals of
Arnold G. Reinhold on http://diceware.com . It generates passphrases
by concatenating words randomly picked from wordlists. For instance::

  $ diceware
  MyraPend93rdSixthEagleAid

The passphrase contains by default six words (with first char
capitalized) without any separator chars. Optionally you can let
`diceware` insert special chars into the passphrase.

`diceware` supports several sources of randomness (including real life
dice) and different wordlists (including cryptographically signed
ones).

.. contents::


Install
-------

This Python package can be installed via pip_::

  $ pip install diceware

The exact way depends on your operating system.


Usage
-----

Once installed, use ``--help`` to list all available options::

  $ diceware --help
  Create a passphrase

  positional arguments:
    INFILE                Input wordlist. `-' will read from stdin.

  optional arguments:
    -h, --help            show this help message and exit
    -n NUM, --num NUM     number of words to concatenate. Default: 6
    -c, --caps            Capitalize words. This is the default.
    --no-caps             Turn off capitalization.
    -s NUM, --specials NUM
                          Insert NUM special chars into generated word.
    -d DELIMITER, --delimiter DELIMITER
                          Separate words by DELIMITER. Empty string by default.
    -r SOURCE, --randomsource SOURCE
                          Get randomness from this source. Possible values:
                          `realdice', `system'. Default: system
    -w NAME, --wordlist NAME
                          Use words from this wordlist. Possible values: `en',
                          `en_eff', `en_orig', `en_securedrop'. Wordlists are
                          stored in the folder displayed below. Default: en_eff
    -v, --verbose         Be verbose. Use several times for increased verbosity.
    --version             output version information and exit.

  Arguments related to `realdice' randomsource:
    --dice-sides N        Number of sides of dice. Default: 6

  Wordlists are stored in <WORDLISTS-DIR>

With ``-n`` you can tell how many words are supposed to be picked for
your new passphrase::

  $ diceware -n 1
  Thud

  $ diceware -n 2
  KnitMargo

You can `diceware` additionally let generate special chars to replace
characters in the 'normal' passphrase.  The number of special chars
generated can be determined with the ``-s`` option (*default is zero*)::

  $ diceware -s 2
  Heroic%unkLon#DmLewJohns

Here ``"%"`` and ``"#"`` are the special chars.

Special chars are taken from the following list::

  ~!#$%^&*()-=+[]\{}:;\"'<>?/0123456789

Please note that several special chars might replace the same original
char, resulting in a passphrase with less special chars than requested.

With ``-d`` you can advise `diceware` to put a delimiter string
between the words generated::

  $ diceware -d "_"
  Wavy_Baden_400_Whelp_Quest_Macon

By default we use the empty string as delimiter, which is good for
copying via double click on Linux systems. But other delimiters might
make your passphrases more readable (and more secure, see
`Security Traps <#sec-traps>`_ below).

By default the single phrase words are capitalized, i.e. the first
char of each word is made uppercase. This does not neccessarily give
better entropy (but protects against entropy loss due to non `prefix
code`_, see `Security Traps <#sec-traps>`_ below), and it might
improve phrase readability.

You can nevertheless disable caps with the ``--no-caps`` option::

  $ diceware --no-caps
  oceanblendbaronferrylistenvalet

This will leave the input words untouched (upper-case stays upper-case,
lower-case stays lower-case). It does *not* mean, that all output words will be
lower-case (except if all words of your wordlist are lowercase).

As the default lists of `diceware` contain only lower-case terms, here
``--no-caps`` means in fact lower-case only output, which might be easier to
type on smart phones and similar.

`diceware` supports also different sources of randomness, which can be
chosen with the ``-r <SOURCENAME>`` or ``--randomsource <SOURCENAME>``
option. Use the ``--help`` option to list all valid values for this
option.

By default we use the `random.SystemRandom`_ class of standard Python
lib but you can also bring your own dice to create randomness::

  $ diceware -r realdice --dice-sides 6
  Please roll 5 dice (or a single dice 5 times).
  What number shows dice number 1? 2
  What number shows dice number 2? 3
  ...
  DogmaAnyShrikeSageSableHoar

Normally dice have six sides. And this is also the default in
`diceware` if you do not use ``--dice-sides``. But if you do, you can
tell how many sides (all) your dice have. More sides will lead to less
rolls required.

We support even sources of randomness from other packages. See the
`documentation <https://diceware.readthedocs.io/>`_ for more details.

`diceware` comes with an English wordlist provided by the EFF_, which will be
used by default and contains 7776 (=6^5) different words. This list is
registered as ``en_eff``.

Additionally `diceware` comes with an English wordlist provided by
`@heartsucker`_, which contains 8192 different words. This list is based off
the original diceware list written by Arnold G. Reinhold.

Both the original and 8k diceware wordlists by Mr. Reinhold are provided.
You can enable a certain (installed) wordlist with the ``-w`` option::

  $ diceware --wordlist en_orig
  YorkNodePrickEchoToriNiobe

See ``diceware --help`` for a list of all installed wordlists.

If you do not like the wordlists provided, you can use your own
one. Any `INFILE` provided will be parsed line by line and each line
considered a possible word. For instance::

  $ echo -e "hi\nhello\n" > mywordlist.txt
  $ diceware mywordlist.txt
  HelloHelloHiHiHiHello

With dash (``-``) as filename you can pipe in wordlists::

  $ echo -e "hi\nhello\n" | diceware -
  HiHiHelloHiHiHello

In custom wordlists we take each line for a valid word and ignore
empty lines (i.e. lines containing whitespace characters only). Oh,
and we handle even PGP-signed wordlists.

You can set customized default values in a configuration file
``.diceware.ini`` (note the leading dot) placed in your home
directory. This file could look like this::

  [diceware]
  num = 7
  caps = off
  specials = 2
  delimiter = "MYDELIMITER"
  randomsource = "system"
  wordlist = "en_securedrop"

The options names have to match long argument names, as output by
``--help``. The values set must meet the requirements valid for
commandline usage. All options must be set within a section
``[diceware]``.


What is it good for?
--------------------

Normally, `diceware` passphrases are easier to remember than shorter
passwords constructed in more or less bizarre ways. But at the same
time `diceware` passphrases provide more entropy as `xkcd`_ can show
with the famous '936' proof_:

.. image:: http://imgs.xkcd.com/comics/password_strength.png
   :align: center
   :target: http://xkcd.com/936/

.. _xkcd: http://xkcd.com/
.. _proof: http://xkcd.com/936/

The standard english wordlist of this `diceware` implementation contains 7776 =
6^5 different english words. It is the official EFF_ wordlist.  compiled by
`Joseph Bonneau`_. Therefore, picking a random word from this list gives an
entropy of nearly 12.9 bits. Picking six words means an entropy of 6 x 12.9 =
77.54 bits.

The special chars replacing chars of the originally created passphrase
give some more entropy (the more chars you have, the more additional
entropy), but not much. For instance, for a sixteen chars phrase you
have sixteen possibilities to place one of the 36 special chars. That
makes 36 x 16 possibilitities or an entropy of about 9.17 you can add.
To get an entropy increase of at least 10 bits, you have to put a
special char in a phrase with at least 29 chars (while at the same
time an additional word would give you 13 bits of extra
entropy). Therefore you might think again about using special chars in
your passphrase.


Is it secure?
-------------

The security level provided by Diceware_ depends heavily on your
source of random. If the delivered randomness is good, then your
passphrases will be very strong. If instead someone can foresee the
numbers generated by a random number generator, your passphrases will
be surprisingly weak.

This Python implementation uses (by default) the
`random.SystemRandom`_ source provided by Python. On Un*x systems it
accesses `/dev/urandom`. You might want to follow reports about
manipulated random number generators in operating systems closely.

The Python API of this package allows usage of other sources of
randomness when generating passphrases. This includes real dice. See
the ``-r`` option.


.. _sec-traps:

Security Traps
--------------

There are issues that might reduce the entropy of the passphrase
generated. One of them is the `prefix code`_ problem:


Prefix Code
...........

If the wordlist contains, for example, the words::

   "air", "airport", "portable", "able"

*and* we switched off caps *and* delimiter chars, then `diceware` might
generate a passphrase containing::

   "airportable"

which could come from ``air-portable`` or ``airport-able``. We cannot
tell and an attacker would have less combinations to guess.

To avoid that, you can leave caps enabled (the default), use any word
delimiter except the empty string or use the ``en_eff`` wordlist,
which was checked to be a `prefix code`_ (i.e. it does not contain
words that start with other words in the list).

Each of these measures is sufficient to protect you against the
`prefix code`_ problem.


Reduced Entropy
...............

Overall, `diceware` is a kind of mapping input values, dice throws for
instance, onto wordlist entries. We normally want each of the words in the
wordlist to be picked for passphrases with the same probability.

This, however, is not possible, if the number of wordlist entries is not a
power of dice sides. In that case we cut some words of the wordlist and inform
the user about the matter. Reducing the number of words this way makes it
easier for attackers to guess the phrase picked.

You can fix that problem by using longer wordlists.


Developer Install
-----------------

Developers want to `fork me on github`_::

  $ git clone https://github.com/ulif/diceware.git

We recommend to create and activate a virtualenv_ first::

  $ cd diceware/
  $ virtualenv -p /usr/bin/python3.4 py34
  $ source py34/bin/activate
  (py34) $

We support Python versions 2.6, 2.7, 3.3 to 3.6, and pypy.

Now you can create the devel environment::

  (py34) $ python setup.py dev

This will fetch test packages (py.test_). You should be able to run
tests now::

  (py34) $ py.test

If you have also different Python versions installed you can use tox_
for using them all for testing::

  (py34) $ pip install tox   # only once
  (py34) $ tox

Should run tests in all supported Python versions.


Documentation Install
.....................

The docs can be generated with Sphinx_. The needed packages are
installed via::

  (py34) $ python setup.py docs

To create HTML you have to go to the ``docs/`` directory and use the
prepared ``Makefile``::

  (py34) $ cd docs/
  (py34) $ make

This should generate the docs in ``docs/_build/html/``.


Creating the Man Page
.....................

We provide a `ReStructuredTexT`_ template to create a man page. When the
documentation engine is installed (`Sphinx`_, see above), then you can create a
manpage doing::

  (py34) $ rst2man.py docs/manpage.rst > diceware.1

The template is mainly provided to ease the job of Debian maintainers.
Currently, it is not automatically updated. Dates, authors, synopsis, etc. have
to be updated manually. Information in the manpage may therefore be wrong,
outdated, or simply misleading.


Credits
-------

Arnold G. Reinhold deserves all merits for the working parts of
`Diceware`_. The non-working parts are certainly my fault.

People that helped spotting bugs, providing solutions, etc.:

 - `Conor Schaefer (conorsch) <https://github.com/conorsch>`_
 - Rodolfo Gouveia suggested to activate the ``--delimiter`` option.
 - `@drebs`_ provided patches and discussion for different sources of
   randomness. `@drebs`_ also initiated and performed the packaging of
   `diceware` for the `Debian`_ platform. Many kudos for this work! `@drebs`_
   is also the official Debian maintainer of the `diceware` package.
 - `@heartsucker`_ hand-compiled and added a new english wordlist.
 - `dwcoder <https://github.com/dwcoder>`_ revealed and fixed bugs
   #19, #21, #23. Also showed sound knowledge of (theoretical)
   entropy. A pleasure to work with.
 - `George V. Reilly <https://github.com/georgevreilly>`_ pointed to new
   EFF wordlists.
 - `lieryan <https://github.com/lieryan>`_ brought up the `prefix
   code`_ problem.
 - `LogosOfJ <https://github.com/LogosOfJ>`_ discovered and fixed
   serious `realdice` source of randomness problem.
 - `Bhavin Gandhi <https://github.com/bhavin192>`_ fixed the confusing error
   message when an invalid input filename is given.

Many thanks to all of them!


Links
-----

- The Diceware_ home page. Reading definitely recommended!
- `fork me on github`_

Wordlists:

_ `Diceware standard list`_ by Arnold G. Reinhold.
- `Diceware8k list`_ by Arnold G. Reinhold.
- `Diceware SecureDrop list`_ by `@heartsucker`_.
- `EFF large list`_ provided by EFF_.


License
-------

This Python implementation of Diceware, (C) 2015-2017 Uli Fouquet, is
licensed under the GPL v3+.

The Copyright for the Diceware_ idea and the `Diceware8k list`_ are Copyright
by Arnold G. Reinhold. The Copyright for the the `Diceware SecureDrop list`_
are copyright by `@heartsucker`_. Copyright for the `EFF large list`_ by
`Joseph Bonneau`_ and EFF_. See file LICENSE for details.

.. _pip: https://pip.pypa.io/en/latest/
.. _`Debian`: https://www.debian.org/
.. _`Diceware`: http://diceware.com/
.. _`Diceware standard list`: http://world.std.com/~reinhold/diceware.wordlist.asc
.. _`Diceware SecureDrop list`: https://github.com/heartsucker/diceware
.. _`Diceware8k list`: http://world.std.com/~reinhold/diceware8k.txt
.. _`@drebs`: https://github.com/drebs
.. _`EFF`: https://eff.org/
.. _`EFF large list`: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
.. _`fork me on github`: http://github.com/ulif/diceware/
.. _`@heartsucker`: https://github.com/heartsucker/
.. _`Joseph Bonneau`: https://www.eff.org/about/staff/joseph-bonneau
.. _`prefix code`: https://en.wikipedia.org/wiki/Prefix_code
.. _`random.SystemRandom`: https://docs.python.org/3.4/library/random.html#random.SystemRandom
.. _ReStructuredText: http://docutils.sourceforge.net/rst.html
.. _virtualenv: https://virtualenv.pypa.io/
.. _py.test: https://pytest.org/
.. _tox: https://tox.testrun.org/
.. _Sphinx: https://sphinx-doc.org/



Changes
=======

0.9.4 (2018-02-27)
------------------

- Set default logging level to ERROR (was: CRITICAL)
- Fixed #44: provide a short and readable file-not-found message (many thanks to
  `bhavin192 <https://github.com/bhavin192>`_)
- Fixed #45: clean up logging handlers after test runs.
- Removed date-dependent tests from default test suite. Run ``py.test -m ''``
  or ``tox`` to run them.


0.9.3 (2017-09-14)
------------------

- Fix broken test.


0.9.2 (2017-09-14)
------------------

- Fixed #33. Make `en_eff` the new default wordlist. This results in slightly
  decreased entropy per word (12.92 bits instead of 13.0), but provides prefix
  code and better memorizable words. Thanks to @anarcat for the suggestion.
- Fixed #35. Make `realdice` source of randomness provide an equal distribution
  of roll numbers even for sequences shorter than number of dice sides.
- Added a man page.
- Support Python 3.6.
- Import `ConfigParser` instead of `SafeConfigParser` if the latter is an alias
  of the former.
- Fixed #37. Ensure file descriptors are closed properly.
- Fixed #38. Get wordlists dir by function (instead of const) to allow
  reproducible builds. Kudos go to @drebs, again.


0.9.1 (2016-12-24)
------------------

- Fixed #32, in docs tell that ``--no-caps`` option does not generate
  lower-case terms.
- Fixed #31, broken `realdice` source of randomness. `argparse` related bug,
  Bug was discovered and fixed by @LogosOfJ, thanks a lot!
- Fixed #29. Tell about code prefix problem in README.
- Activated logging. Using `verbose` will result in additional output.


0.9 (2016-09-14)
----------------

- Added `--dice-sides` option to tell how many sides used dices
  provide.
- Changed API interface of `get_config_dict()` to allow more flexible
  handling of config files.
- Support different verbosity levels.
- Added new wordlist ``en_eff``. It is a 7776-terms list provided by
  the Electronic Frontier Foundation. See
  https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
  for details. Thanks to `George V. Reilly
  <https://github.com/georgevreilly>`_ for hinting!
- Fixed #27. Allow dashes in numbered wordlists. Yet, these looked
  like ``1234 myterm``. We now also accept ``1-2-3-4 myterm``.


0.8 (2016-05-07)
----------------

- Closed #23. @dwcoder provided a fix that allows use of
  whitespace-only values in diceware confg files if they are enclosed
  in quotes.
- Fixed #21. @dwcoder revealed and fixed (again!). This time `--caps`
  and `--no-caps` settings did not work properly when set in CLI or in
  `.diceware.ini` config file.
- Shortened real-dice randomness source.
- Added logger as common interface to send messages to users.
- New dependency: `sphinx_rtd_theme` for generating docs. This theme
  was formerly a dependency of `Sphinx`.


0.7.1 (2016-04-21)
------------------

- Fixed #19. @dwcoder revealed and fixed a nasty bug in the real-dice
  randomness-source. Thanks a lot!


0.7 (2016-04-17)
----------------

- Added sample ``.diceware.ini``.
- Added new english wordlist ``en_securedrop``. This is the new
  default list. Thanks to `heartsucker
  <https://github.com/heartsucker>`_ who compiled and added the list.
- Remove support for Python 3.2. Several packages we depend on for testing
  and sandboxing stopped Python 3.2 support. We follow them.


0.6.1 (2015-12-15)
------------------

- Minor doc changes: add separate config file docs.
- Fix docs: the default wordlist is named ``en``. Some docs were not
  up-to-date in that regard.


0.6 (2015-12-15)
----------------

- Officially support Pyhthon 3.5.
- Tests do not depend on `pytest-cov`, `pytest-xdist` anymore.
- Support configuration files. You can set different defaults in a
  file called ``.diceware.ini`` in your home directory.
- Renamed wordlist ``en_8k`` to ``en`` as it serves as the default
  for english passphrases.


0.5 (2015-08-05)
----------------

- New option ``-r``, ``--randomsource``. We support a pluggable system
  to define alternative sources of randomness. Currently supported
  sources: ``"system"`` (to retrieve randomness from standard library,
  default) and ``realdice``, which allows use of real dice.
- New option ``-w``, ``--wordlist``. We now provide several wordlists
  for users to choose from. Own wordlists could already be fed to
  `diceware` before. By default we still use the 8192 words list from
  http://diceware.com.
- Rename `SRC_DIR` to `WORDLISTS_DIR` (reflecting what it stands for).
- Use also flake8 with tox.
- Pass `options` to `get_passphrase()` instead of a bunch of single args.
- Output wordlists dir in help output.


0.4 (2015-03-30)
----------------

- Add --delimiter option (thanks to Rodolfo Gouveia).


0.3.1 (2015-03-29)
------------------

- Turned former `diceware` module into a Python package. This is to
  fix `bug #1 Wordlists aren't included during installation
  <https://github.com/ulif/diceware/issues/1>`_, this time really.
  Wordlists will from now on be stored inside the `diceware` package.
  Again many thanks to `conorsch <https://github.com/conorsch>`_ who
  digged deep into the matter and also came up with a very considerable
  solution.
- Use readthedocs theme in docs.


0.3 (2015-03-28)
----------------

- Fix `bug #1 Wordlists aren't included during installation
  <https://github.com/ulif/diceware/issues/1>`_ . Thanks to `conorsch
  <https://github.com/conorsch>`_
- Add --version option.


0.2 (2015-03-27)
----------------

- Minor documentation changes.
- Updated copyright infos.
- Add support for custom wordlists.


0.1 (2015-02-18)
----------------

- Initial release.


