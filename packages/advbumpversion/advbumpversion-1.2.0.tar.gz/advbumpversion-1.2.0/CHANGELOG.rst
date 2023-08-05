.. _changelog:

Changes
=======

**v1.2.0**

- Add ``independent`` flag for version parts. This part is not reset when other parts are incremented. For example, for
  build numbers
- Add EXAMPLES.rst with several test cases
- Add new test cases: update version and build date, build number, annotated tags, test cases for almost all cases in
  EXAMPLES.rst

**v1.1.1**

- Fix a bug with PR#117: allow multiple config sections per file. Add a test case.

**v1.1.0**

- Compatibility with Travis CI
- Publish on PyPi

**v1.0.0**

Fork of fork. The project is renamed **advbumpversion** to avoid confusion with other forks.
The following Push requests are merged in this project:

- `PR#8 <https://github.com/c4urself/bump2version/pull/8>`_ from @ekoh: Add Python 3.5 and 3.6 to the supported versions: Add Python 3.5 and 3.6 to the supported versions
- `PR#117 <https://github.com/peritus/bumpversion/pull/117>`_ from from @chadawagner: allow multiple config sections per file
- `PR#136 <https://github.com/peritus/bumpversion/pull/136>`_ from @vadeg: Fix documentation example with 'optional_value'
- `PR#138 <https://github.com/peritus/bumpversion/pull/138>`_ from @smsearcy: Fixes TypeError in Python 3 on Windows
- `PR#157 <https://github.com/peritus/bumpversion/pull/157>`_ from todd-dembrey: Fix verbose tags

I consider this project stable enough to raise the version to 1.0.0.

**v0.5.7**

- Added support for signing tags (git tag -s)
  thanks: @Californian (`#6 <https://github.com/c4urself/bump2version/pull/6>`_)

**v0.5.6**

- Added compatibility with `bumpversion` by making script install as `bumpversion` as well
  thanks: @the-allanc (`#2 <https://github.com/c4urself/bump2version/pull/2>`_)

**v0.5.5**

- Added support for annotated tags
  thanks: @ekohl @gvangool (`#58 <https://github.com/peritus/bumpversion/pull/58>`_)

**v0.5.4**

- Renamed to bump2version to ensure no conflicts with original package

**v0.5.3**

- Fix bug where ``--new-version`` value was not used when config was present
  (thanks @cscetbon @ecordell (`#60 <https://github.com/peritus/bumpversion/pull/60>`_)
- Preserve case of keys config file
  (thanks theskumar `#75 <https://github.com/peritus/bumpversion/pull/75>`_)
- Windows CRLF improvements (thanks @thebjorn)

**v0.5.1**

- Document file specific options ``search =`` and ``replace =`` (introduced in 0.5.0)
- Fix parsing individual labels from ``serialize =`` config even if there are
  characters after the last label (thanks @mskrajnowski `#56
  <https://github.com/peritus/bumpversion/pull/56>`_).
- Fix: Don't crash in git repositories that have tags that contain hyphens
  (`#51 <https://github.com/peritus/bumpversion/pull/51>`_) (`#52
  <https://github.com/peritus/bumpversion/pull/52>`_).
- Fix: Log actual content of the config file, not what ConfigParser prints
  after reading it.
- Fix: Support multiline values in ``search =``
- also load configuration from ``setup.cfg`` (thanks @t-8ch `#57
  <https://github.com/peritus/bumpversion/pull/57>`_).

**v0.5.0**

This is a major one, containing two larger features, that require some changes
in the configuration format. This release is fully backwards compatible to
*v0.4.1*, however deprecates two uses that will be removed in a future version.

- New feature: `Part specific configuration <#part-specific-configuration>`_
- New feature: `File specific configuration <#file-specific-configuration>`_
- New feature: parse option can now span multiple line (allows to comment complex
  regular expressions. See `re.VERBOSE in the Python documentation
  <https://docs.python.org/library/re.html#re.VERBOSE>`_ for details, `this
  testcase
  <https://github.com/peritus/bumpversion/blob/165e5d8bd308e9b7a1a6d17dba8aec9603f2d063/tests.py#L1202-L1211>`_
  as an example.)
- New feature: ``--allow-dirty`` (`#42 <https://github.com/peritus/bumpversion/pull/42>`_).
- Fix: Save the files in binary mode to avoid mutating newlines (thanks @jaraco `#45 <https://github.com/peritus/bumpversion/pull/45>`_).
- License: bumpversion is now licensed under the MIT License (`#47 <https://github.com/peritus/bumpversion/issues/47>`_)

- Deprecate multiple files on the command line (use a `configuration file <#configuration>`_ instead, or invoke ``bumpversion`` multiple times)
- Deprecate 'files =' configuration (use `file specific configuration <#file-specific-configuration>`_ instead)

**v0.4.1**

- Add --list option (`#39 <https://github.com/peritus/bumpversion/issues/39>`_)
- Use temporary files for handing over commit/tag messages to git/hg (`#36 <https://github.com/peritus/bumpversion/issues/36>`_)
- Fix: don't encode stdout as utf-8 on py3 (`#40 <https://github.com/peritus/bumpversion/issues/40>`_)
- Fix: logging of content of config file was wrong

**v0.4.0**

- Add --verbose option (`#21 <https://github.com/peritus/bumpversion/issues/21>`_ `#30 <https://github.com/peritus/bumpversion/issues/30>`_)
- Allow option --serialize multiple times

**v0.3.8**

- Fix: --parse/--serialize didn't work from cfg (`#34 <https://github.com/peritus/bumpversion/issues/34>`_)

**v0.3.7**

- Don't fail if git or hg is not installed (thanks @keimlink)
- "files" option is now optional (`#16 <https://github.com/peritus/bumpversion/issues/16>`_)
- Fix bug related to dirty work dir (`#28 <https://github.com/peritus/bumpversion/issues/28>`_)


**v0.3.6**

- Fix --tag default (thanks @keimlink)

**v0.3.5**

- add {now} and {utcnow} to context
- use correct file encoding writing to config file. NOTE: If you are using
  Python2 and want to use UTF-8 encoded characters in your config file, you
  need to update ConfigParser like using 'pip install -U configparser'
- leave current_version in config even if available from vcs tags (was
  confusing)
- print own version number in usage
- allow bumping parts that contain non-numerics
- various fixes regarding file encoding

**v0.3.4**

- bugfix: tag_name and message in .bumpversion.cfg didn't have an effect (`#9 <https://github.com/peritus/bumpversion/issues/9>`_)

**v0.3.3**

- add --tag-name option
- now works on Python 3.2, 3.3 and PyPy

**v0.3.2**

- bugfix: Read only tags from `git describe` that look like versions

**v0.3.1**

- bugfix: ``--help`` in git workdir raising AssertionError
- bugfix: fail earlier if one of files does not exist
- bugfix: ``commit = True`` / ``tag = True`` in .bumpversion.cfg had no effect

**v0.3.0**

- **BREAKING CHANGE** The ``--bump`` argument was removed, this is now the first
  positional argument.
  If you used ``bumpversion --bump major`` before, you can use
  ``bumpversion major`` now.
  If you used ``bumpversion`` without arguments before, you now
  need to specify the part (previous default was ``patch``) as in
  ``bumpversion patch``).

**v0.2.2**

- add --no-commit, --no-tag

**v0.2.1**

- If available, use git to learn about current version

**v0.2.0**

- Mercurial support

**v0.1.1**

- Only create a tag when it's requested (thanks @gvangool)

**v0.1.0**

- Initial public version
