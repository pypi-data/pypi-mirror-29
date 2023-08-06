## gpsd-python3
----

Simple port of the official GPSD project libraries to a separate package.

Python files match the 3.17 release, and if conflicts arise, the [ GPSD Project ]( http://www.catb.org/gpsd/ ) will be more up-to-date.

## Motivation

The GPSD project has supported python2 for many years, but python3 support is
much more recent.  Unfortunately, because GPSD uses SCons as its build system,
building with, and installing client libraries for python 3 requires scons 3.0+.

Until such support is more widespread, this package provides an appropriate stop-gap.

Use this package if you:
1. Use GPSD client libraries
2. Implement in python 3;
3. have one of the following:
  - Don't need a full gpsd install, just the client libraries
  - Running Ubuntu 17.10 or lower
  - Otherwise have SCons 3.0 or lower installed

If you don't have one of these situations, the Official GPSD project will probably
satisfy your needs.

----
All code is covered under the BSD license with rights assigned to the GPSD Project.
