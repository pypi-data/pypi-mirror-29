Change Log For PyCliProg
========================


PyCliProg 0.3.0 - 2018-03-01
----------------------------

- Major breaking changes

  - ``pycliprog`` is now a namespace package

    Use ``pycliprog.argparse`` wherever you use ``pycliprog`` before this change.

- Added names

  - ``Prog#read_desc``
  - ``Prog#read_prop``

- Other changes

  - ``Prog#read_version`` now accepts ``*args`` which are passed to ``os.path.join``
  - Merged ``logging level`` & ``logging file`` group into ``logging control``


PyCliProg 0.2.0 - 2017-08-08
----------------------------

- Removed names

  - throwing ``ArgumentParser`` & ``ArgError``
  - ``Prog.add_basic_args``

    - Merged into ``Prog.add_logging_args``
    - Renamed to ``Prog.add_common_args``
    - Placed after the call of ``self.add_args``

- Added names

  - ``Prog#read_version``
  - A logger is available via ``self.logger``
  - Some properties

    - ``Prog.name``
    - ``Prog.desc``
    - ``Prog.epilog``
    - ``Prog.fmtcls``
    - ``Prog.version``

- Added shorthands

  - ``Prog.add_arg``
  - ``Prog.add_group``

- Other Changes

  - Used help messages in lowercase and without full stops
  - Used ``RawTextHelpFormatter`` by default
  - Removed the short option ``-L``, the long option unchanged
  - Removed the short option ``-A``, the long option unchanged
  - Fixed ``--append-log`` to be a ``store_true`` action
  - Grouped the options ``-v/--verbose`` and ``-q/--quiet`` into ``logging levels``, ``--log-file`` and ``--append-log`` into ``logging files``


PyCliProg 0.1.0 - 2017-03-30
----------------------------

``0.1.0`` is the first public pre-release.

- Added names that are considered public

  - the ``Prog`` class
  - the ``ExitFailure`` exception class

  You won't be prevented from importing any other names,
  but the aforementioned two are the most useful ones.

- Methods that are considered public and should be overridden

  - ``Prog.main``
  - ``Prog.add_args``

  Other methods are considered advanced,
  but not reserved nor internal.
