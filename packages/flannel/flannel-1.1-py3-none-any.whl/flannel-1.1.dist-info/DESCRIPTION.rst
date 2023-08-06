============================

`Repository <https://bitbucket.org/bear_belly/flannel>`__

For JSON addicts, it can sometimes be a bit tricky to read
JSON-formatter log output.

::

    {
      "name": "blue",
      "msg": "carry kid personal visit must table %s but machine other majority dog often avoid ever into %s now speech might when travel process everybody between structure group into behavior red especially staff energy condition somebody deal source %s %s very fish what final %s",
      "args": [
        "almost",
        "resource",
        "suffer",
        "build",
        "stop"
      ],
      "levelname": "ERROR",
      "levelno": "40",
      "pathname": "/thus/get/network/character/use/consumer/main",
      "filename": "middle.py",
      "module": "north",
      "exc_info": "None",
      "exc_text": "None",
      "stack_info": "None",
      "lineno": "1967",
      "funcName": "involve",
      "created": "9366883292.60978",
      "msecs": "708.5866876106",
      "relativeCreated": "766.580321207097",
      "thread": "284803497762",
      "threadName": "MainThread",
      "processName": "MainProcess",
      "process": "16475"
    }

I know, doesn’t look that pleasing. That’s why I created a GUI
application to display JSON logs in a table.

Note that this application can ready *any* set of json data. It’s just
mainly useful for JSON log output.

Need a Handy JSON Logger?
~~~~~~~~~~~~~~~~~~~~~~~~~

Well, thought you’d never ask.

I actually created one

Why The Name “Flannel?”
~~~~~~~~~~~~~~~~~~~~~~~

That’s what loggers (lumberjacks) wear of course!

|Logger|

.. raw:: html

   <p>

 `[1] <https://flic.kr/p/j7aqhp>`__ `Bearded LumberJack
Look <https://www.flickr.com/photos/jeepersmedia/11884158495>`__ `CC BY
2.0 <https://creativecommons.org/licenses/by/2.0/legalcode>`__

.. raw:: html

   </p>

And hipsters.

|Man In Plaid Shirt|

.. raw:: html

   <p>

 `[2] <https://www.flickr.com/people/57864400@N00>`__ `Man in plaid
shirt <https://commons.wikimedia.org/wiki/File:Man_in_plaid_shirt.jpg>`__
`CC BY 2.0 <https://creativecommons.org/licenses/by/2.0/legalcode>`__

.. raw:: html

   </p>

Basic Usage
-----------

Flannel takes the input from standard input (stdin), meaning, to read
JSON output, pipe what you want from another command:

::

    $ ./do-this-thing | flannel

Already have a log file you’d like to read? Don’t need that much extra
work done:

::

    $ cat myfile.log | flannel

If you play your cards right the following window should appear:

A few things to note:

-  Each key in the json log entry corresponds to

   -  A field in the **filter content** section.
   -  A header in the table

-  The **Show Table Headings** is an entry, where you can type in any
   field listed (comma seperated) and the table will show only those
   columns you specify. You can also order the columns.
-  Sometimes a program may spit out strings not in json format. That’s
   why I included the **Raw Output** tab, so that if things aren’t
   working out, you can see what went wrong. Note this is the raw output
   for *your program*, not for *flannel*.

.. figure:: ./doc/images/flannel-basic-example.png
   :alt: Flannel Window

   Flannel Window

Not Seeing Anything in Flannel?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Firstly, you read the *Basic Usage* section, right? You need to feed in
from stdin. ;-)

Now that you have that covered…

I was a a bit confused myself, and I designed this thing!

It’s not an issue with flannel, but, rather, with how UNIX handles
standard input and output. When a program writes content to the
terminal, only stdout is piped. A program will typically write log
entries to ``stderr``, which is not piped to ``stdin``.

**tl;dr:** Do this instead:

::

    $ ./do-this-thing 2>&1 | flannel

Notice the **2>&1**. That redirects stderr to stdout. Then you should
see output.

Log slowing down?
~~~~~~~~~~~~~~~~~

You might not want to keep *all* the logs in memory. Hitting the
``[Clear]`` button next to the output table should–er–clear things up.

Requirements
------------

-  Python 3+
-  PyQt5 and up
-  Lord of the Config

Optionally, faker is used for the testing module
``flannel.json_output``.

Installation
------------

Install as you would other python packages:

::

    $ pip install flannel

.. |Logger| image:: ./doc/images/flannel-man.jpg
.. |Man In Plaid Shirt| image:: ./doc/images/Man_in_plaid_shirt.jpg


Home-page: UNKNOWN
Author: Jordan Hewitt
Author-email: jordan.h@startmail.com
License: GPLv3
Description-Content-Type: UNKNOWN
Description: UNKNOWN
Keywords: flannel qt lot viewer gui application app logging
Platform: UNKNOWN
