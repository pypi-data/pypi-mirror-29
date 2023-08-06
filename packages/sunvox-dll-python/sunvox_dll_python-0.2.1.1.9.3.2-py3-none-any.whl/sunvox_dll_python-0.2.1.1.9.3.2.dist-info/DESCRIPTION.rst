Overview of sunvox-dll-python
=============================



Part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/


Purpose
-------

Provides access to all of the SunVox DLL functions described
in the ``sunvox.h`` header file.




Requirements
------------

- Python 3.5

- One of these supported operating systems:

    - macOS (64-bit)

    - Linux (32-bit, 64-bit)

    - Windows (32-bit, 64-bit)


About SunVox
------------

From the `SunVox home page`_:

    SunVox is a small, fast and powerful modular synthesizer with pattern-based sequencer (tracker).
    It is a tool for those people who like to compose music wherever they are, whenever they wish.
    On any device. SunVox is available for Windows, OS X, Linux, Maemo, Meego, Raspberry Pi,
    Windows Mobile (WindowsCE), PalmOS, iOS and Android.

.. _SunVox home page: http://www.warmplace.ru/soft/sunvox/

Changelog
=========


0.2.1.1.9.3.2 (2018-02-28)
--------------------------

- Add Raspberry Pi version of SunVox DLL.

- Add ``sunvox.SUNVOX_COPYRIGHT_NOTICE`` constant, for use in apps
  that make use of this package.


0.2.0.1.9.3.1 (2017-11-25)
--------------------------

- Update SunVox DLL to 1.9.3b (1.9.3.1).


0.2.0.1.9.3.0 (2017-11-25)
--------------------------

- Update SunVox DLL to 1.9.3.0.

- Add support for Windows 64-bit.

- Correct notation of sharps/flats to match SunVox.

- Improvements to buffered processes.


0.1.0.1.9.2.0 (2016-11-08)
--------------------------

- Initial release.


