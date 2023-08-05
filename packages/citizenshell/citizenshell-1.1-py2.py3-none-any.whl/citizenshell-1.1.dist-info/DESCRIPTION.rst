citizenshell |Build Status|
===========================

**citizenshell** is (or rather will be) a python library allowing to
execute shell commands either locally or remotely over several protocols
(telnet, ssh, serial or adb) using a simple and consistent API. This
library is compatible with both python 2 (2.7) and 3 (>=3.4) as well as
with `PyPy <https://pypy.org/>`__. For now, it focuses on POSIX
platforms like Linux and MacOS, but may be extended to work to Windows
based platform in the future. It is distributed under
`MIT <https://opensource.org/licenses/MIT>`__ license.

Roadmap
-------

Version 1.0
~~~~~~~~~~~

-  [x] local shell
-  [x] shell over ssh using `paramiko <http://www.paramiko.org/>`__
-  [x] shell over telnet using
   `telnetlib <https://docs.python.org/2/library/telnetlib.html>`__
-  [x] shell over
   `adb <https://developer.android.com/studio/command-line/adb.html>`__
-  [x] shell over serial using
   `pyserial <https://github.com/pyserial/pyserial>`__
-  [x] possibility to open shell by uri
-  [x] support for logging with colored formatter
-  [x] available from PIP repository

Version 1.1
~~~~~~~~~~~

-  [ ] add support for pushing (upload) and pulling (download) files for
   ``AdbShell`` using
   `adb <https://developer.android.com/studio/command-line/adb.html>`__
-  [ ] add support for pushing (upload) and pulling (download) files for
   ``TelnetShell`` using `netcat <https://linux.die.net/man/1/nc>`__
-  [ ] add support for pushing (upload) and pulling (download) files for
   ``SecureShell`` using `paramiko <http://www.paramiko.org/>`__
-  [ ] add support for pushing (upload) and pulling (download) files for
   ``SerialShell`` using `rz <https://linux.die.net/man/1/rz>`__

Examples
--------

LocalShell
~~~~~~~~~~

you can use the built-in ``sh`` command for simple commands:

.. code:: python

    from citizenshell import sh

    assert sh("echo Hello World") == "Hello World"

you can instanciate a ``LocalShell`` for more complex cases:

.. code:: python

    from citizenshell import LocalShell

    shell = LocalShell(GREET="Hello")
    assert shell("echo $GREET $WHO", WHO="Citizen") == "Hello Citizen"

you can also iterate over stdout:

.. code:: python

    from citizenshell import LocalShell

    shell = LocalShell()
    result = [int(x) for x in shell("""
        for i in 1 2 3 4; do
            echo $i;
        done
    """)]
    assert result == [1, 2, 3, 4]

or you can extract stdout, stderr and exit code seperately:

.. code:: python

    from citizenshell import LocalShell

    shell = LocalShell()
    result = shell(">&2 echo error && echo output && exit 13")
    assert result.out == ["output"]
    assert result.err == ["error"]
    assert result.xc == 13

TelnetShell
~~~~~~~~~~~

you can instanciate the ``TelnetShell`` for shell over telnet:

.. code:: python

    from citizenshell import TelnetShell

    shell = TelnetShell(hostname="acme.org", username="john", password="secretpassword")
    assert shell("echo Hello World") == "Hello World"

you can then do eveything you can do with a ``LocalShell``.

SecureShell
~~~~~~~~~~~

you can instanciate the ``SecureShell`` for shell over SSH:

.. code:: python

    from citizenshell import SecureShell

    shell = SecureShell(hostname="acme.org", username="john", password="secretpassword")
    assert shell("echo Hello World") == "Hello World"

you can then do eveything you can do with a ``LocalShell``. Beware that
some SSH servers refuse to set environment variable (see documentation
of AcceptEnv of
`sshd\_config <https://linux.die.net/man/5/sshd_config>`__ and
documentation of ``update_environment`` of `paramiko's ``Channel``
class <http://docs.paramiko.org/en/2.4/api/channel.html>`__) and that
will fail silently.

AdbShell
~~~~~~~~

you can instanciate the ``AdbShell`` for shell over ADB:

.. code:: python

    from citizenshell import AdbShell

    shell = AdbShell(hostname="acme.org", username="john", password="secretpassword")
    assert shell("echo Hello World") == "Hello World"

you can then do eveything you can do with a ``LocalShell``.

SerialShell
~~~~~~~~~~~

you can instanciate the ``SerialShell`` for shell over serial line:

.. code:: python

    from serial import EIGHTBITS, PARITY_NONE
    from citizenshell import SerialShell

    shell = SerialShell(port="/dev/ttyUSB3", username="john", password="secretpassword", baudrate=115200, parity=PARITY_NONE, bytesize=EIGHTBITS)
    assert shell("echo Hello World") == "Hello World"

you can then do eveything you can do with a ``LocalShell``.

Shell
~~~~~

you can also obtain shell objects by URI using the ``Shell`` function:

.. code:: python

    from citizenshell import Shell

    localshell = Shell() 
    telnetshell = Shell("telnet://john:secretpassword@acme.org:1234")
    secureshell = Shell("ssh://john:secretpassword@acme.org:1234")
    adbshell = Shell("adb://myandroiddevice:5555")
    serialshell = Shell("serial://jogn:secretpassword@/dev/ttyUSB3?baudrate=115200")

you can mix and match betweens providing arguments in the URI or via
kwargs:

.. code:: python

    from citizenshell import Shell

    localshell = Shell() 
    telnetshell = Shell("telnet://john@acme.org", password="secretpassword", port=1234)
    serialshell = Shell("serial://jogn:secretpassword@/dev/ttyUSB3", baudrate=115200)

you can then use the shell objects as you would any other.

.. |Build Status| image:: https://travis-ci.org/meuter/citizenshell.svg?branch=master
   :target: https://travis-ci.org/meuter/citizenshell


