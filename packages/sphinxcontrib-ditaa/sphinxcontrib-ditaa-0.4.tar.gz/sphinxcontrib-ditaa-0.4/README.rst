sphinxcontrib-ditaa
*********************

A sphinx extension for embedding ditaa diagram.

:author: "Yongping Guo"<guoyoooping@163.com>

1. Introduction
===============

ditaa_ is a small command-line utility that can convert diagrams drawn
using ascii art ('drawings' that contain characters that resemble lines
like | / - ), into proper bitmap graphics. See
http://ditaa.sourceforge.net/, 

This extensions allows rendering of diagram using the ditaa_ to by included in
Sphinx-generated. This extensions adds the ``ditaa`` directive that will
replace the ascii diagram with the image of the ditaa. 

ditaa_ is in java, normal it's call by the following format::

    java  -jar /usr/local/Cellar/ditaa/0.10/libexec/ditaa0_10.jar art10.txt art10.png 

You should convert and call it as:

    ditaa art10.txt art10.png 

If you don't like the converttion, please refer to `4.2 Configuration`_ for
workaround. One possilbe convertation might be like this::

    $ cat /usr/local/bin/ditaa
    #!/bin/bash
    exec java  -jar /usr/local/Cellar/ditaa/0.10/libexec/ditaa0_10.jar "$@"

2. Installing and setup
=======================

pip install sphinxcontrib-ditaa

Just add ``sphinxcontrib.ditaa`` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['sphinxcontrib.ditaa']

3. Quick Example
================

This source::

    .. ditaa::

        +--------+   +-------+    +-------+
        |        | --+ ditaa +--> |       |
        |  Text  |   +-------+    |diagram|
        |Document|   |!magic!|    |       |
        |     {d}|   |       |    |       |
        +---+----+   +-------+    +-------+
            :                         ^
            |       Lots of work      |
            +-------------------------+

is rendered as: |example1|_

.. |example1| image:: http://ditaa.sourceforge.net/images/first.png
.. _example1: http://ditaa.sourceforge.net/images/first.png


Another example::

    .. ditaa::

        +----------+ edit +----------+   input +----------+ compile +----------+
        |  cPNK    |      |  cRED    |         |   cGRE   |         |  cPNK    |
        | refined  |<-----+ h,cpp    +-------->+ compiler,+-------->+Executable|
        |   h,cpp  |      |          |         | linker   |         |   File   |
        |          |      |          |         |          |         |          |
        +----------+      +----+-----+         +----------+         +----------+
                               | input
                               v
                          +----------+
                          |  cGRE    |
                          | doxygen  |
                          |          |
                          +----+-----+
                               | process
                               v
                          +----------+
                          |  cPNK    |
                          | Doxgen   |
                          | Document |
                          |          |
                          +----------+

is rendered as: |example2|_

.. |example2| image:: http://emacser.com/uploads/asciiExampleWithColorAndType.png
.. _example2: http://emacser.com/uploads/asciiExampleWithColorAndType.png

4. Usage
========

1) Firstly, make a directory and write the .rst files::

    $ mkdir test_dir
    $ cd test_dir
    $ vim test.rst

2) create a sphinex project in the directory, presss Enter if there is no
change::

    $ sphinx-quickstart

3) Just add ``sphinxcontrib.ditaa`` to the list of extensions in the
``conf.py`` file just created in step 2::

    extensions = ['sphinxcontrib.ditaa']

4) Add your work .rst files into index.rst just created in step 2::

    Contents:
     
    .. toctree::
       :maxdepth: 2
     
       test.rst

5) make your target files::

    $ make html

or::

    $ make pdf

6) check your target files:

    $ open .build/html/index.html

4.1 Options
-----------

1) ditaa options:

See detail in ditaa -h::

    :--no-antialias:
    :--background:
    :--no-antialias:
    :--no-separation:
    :--encoding:
    :--html:
    :--overwrite:
    :--round-corners:
    :--no-shadows:
    :--scale: 1.5 #Please note that it's ditaa's parameter and the units are
               fractions of the default size (2.5 renders 1.5 times bigger
               than the default). Be warning to be different from image's
               scale unit.
    :--transparent:
    :--tabs:
    :--fixed-slope:

2) image options:

See detail in rst syntax::

    :name: 
    :class: 
    :alt: 
    :title:
    :height: 
    :width: 
    :scale: 50%, Please node that it's integer percentage (the "%" symbol is optional)
    :align: 
    :target: 
    :inline: 

Examples::

    .. ditaa::
       :--no-antialias:
       :--transparent: 
       :--scale: 1.5
       :alt: a test for ditaa.
       :width: 600
       :height: 400
       :align: left
       :scale: 50

        Color codes
        /-------------+-------------\
        |cRED RED     |cBLU BLU     |
        +-------------+-------------+
        |cGRE GRE     |cPNK PNK     |
        +-------------+-------------+
        |cBLK BLK     |cYEL YEL     |
        \-------------+-------------/

4.2 Configuration
-----------------

For now some optional configurations is added to Sphinx_. It can be set in
``conf.py`` file:

``ditaa`` <str>:

    Ditaa is a java implementation and maybe is not callable directly, please
    input the ditaa executale name if you didn't convert it to a normal
    command. Default is "ditaa". See examples below.

``ditaa_args`` <list>:

    Given a ditaa option list, default is empty.

``ditaa_log_enable`` <Bool>:

    Since ditaa is slow, will give out a log to note progress if it's
    configured. Default is True.

::

    ditaa = "java"
    ditaa_args = ["-jar", "/usr/local/Cellar/ditaa/0.10/libexec/ditaa0_10.jar"]
    ditaa_log_enable = True

5. License
==========

GPLv3

.. _ditaa: http://ditaa.sourceforge.net/
.. _Sphinx: http://sphinx.pocoo.org/
