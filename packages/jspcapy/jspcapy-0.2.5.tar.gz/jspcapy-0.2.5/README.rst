.. _header-n0:

jspcapy
=======

    This program depends on
    ```jspcap`` <https://github.com/JarryShaw/jspcap>`__ and
    ```jsformat`` <https://github.com/JarryShaw/jsformat>`__.

 ``jspcapy`` is a **command line** pcap file analyser tool. It supports
analysis on several networking protocol headers, such as ``IP`` (both
version 4 and 6), ``ICMP``, ``TCP``, ``UDP``, ``SCTP``, et al and
streaming output of ``plist``, ``json`` and *tree-view* ``text`` file.

 Notice that the whole project works on Python versions **since 3.6**.

--------------

.. _header-n10:

Installation
------------

 Simply run the following to install the latest from PyPI:

.. code:: shell

    $ pip install jspcapy

 Or install from the git repository:

.. code:: shell

    $ git clone https://github.com/JarryShaw/jspcapy.git
    $ python setup.py install

.. _header-n19:

Usage
-----

 As it shows in the help manual, it is quite easy to use:

.. code:: shell

    $ jspcapy -h
    usage: jspcapy.py [-h] [-v] [-o file-name] [-f format] [-j] [-p] [-t] [-a]
                      [-V]
                      input-file-name

    PCAP file extractor and formatted exporter

    positional arguments:
      input-file-name       The name of input pcap file. If ".pcap" omits, it will
                            be automatically appended.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -o file-name, --output file-name
                            The name of input pcap file. If format extension
                            omits, it will be automatically appended.
      -f format, --format format
                            Print a extraction report in the specified output
                            format. Available are all formats supported by
                            jsformat, e.g.: json, plist, tree, xml, html.
      -j, --json            Display extraction report as json. This will yield
                            "raw" output that may be used by external tools. This
                            option overrides all other options.
      -p, --plist           Display extraction report as macOS Property List
                            (plist). This will yield "raw" output that may be used
                            by external tools. This option overrides all other
                            options.
      -t, --tree            Display extraction report as tree view text. This will
                            yield "raw" output that may be used by external tools.
                            This option overrides all other options.
      -a, --auto-extension  If output file extension omits, append automatically.
      -V, --verbose         Show more information.

 Under most circumstances, you should indicate the name of input pcap
file (extension may omit) and at least, output format (``json``,
``plist``, ``tree``, ``xml``, or ``html``). Once format unspecified, the
name of output file must have proper extension (``*.json``, ``*.plist``,
``*.txt``, ``*.xml``, or ``*.js``), otherwise ``FormatError`` will
raise.

 As for ``verbose`` mode, detailed information will print while
extraction (as following examples). And ``auto-extension`` flag works
for the output file, to indicate whether extensions should be appended.

.. _header-n29:

Samples
-------

 Here are some usage samples:

-  export to a macOS Property List (``Xcode`` has special support for
   this format)

.. code:: shell

     $ jspcapy in -f plist -V
     🚨Loading file 'in.pcap'
      - Frame   1: Ethernet:IPv6:ICMPv6
      - Frame   2: Ethernet:IPv6:ICMPv6
      - Frame   3: Ethernet:IPv4:TCP
      - Frame   4: Ethernet:IPv4:TCP
      - Frame   5: Ethernet:IPv4:TCP
      - Frame   6: Ethernet:IPv4:UDP
     🍺Report file stored in 'out.plist'

-  export to a json file (with no format specified)

.. code:: shell

     $ jspcapy in -o out.json -V
     🚨Loading file 'in.pcap'
     - Frame   1: Ethernet:IPv6:ICMPv6
     - Frame   2: Ethernet:IPv6:ICMPv6
     - Frame   3: Ethernet:IPv4:TCP
     - Frame   4: Ethernet:IPv4:TCP
     - Frame   5: Ethernet:IPv4:TCP
     - Frame   6: Ethernet:IPv4:UDP
    🍺Report file stored in 'out.json'

-  export to a text tree view file (without extension autocorrect)

.. code:: shell

     $ jspcapy in -o out -f tree -V
     🚨Loading file 'in.pcap'
     - Frame   1: Ethernet:IPv6:ICMPv6
     - Frame   2: Ethernet:IPv6:ICMPv6
     - Frame   3: Ethernet:IPv4:TCP
     - Frame   4: Ethernet:IPv4:TCP
     - Frame   5: Ethernet:IPv4:TCP
     - Frame   6: Ethernet:IPv4:UDP
    🍺Report file stored in 'out'
