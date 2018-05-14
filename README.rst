####################################################
Embedded Base Boot Requirements (EBBR) specification
####################################################

The Embedded Base Boot Requirements specification defines requirements
for embedded systems to enable inter-operability between SoCs, hardware
platforms, firmware implementations, and operating system distributions.
The aim is to establish consistent boot ABIs and behaviour so that
supporting new hardware platforms does not require custom engineering work.

EBBR is currently being drafted. The first formal release of EBBR is
expected in September 2018. You can find the current draft text in this
repository, but be aware that everything in the draft text is subject to
change before an official v1.0 release is published.

Build Instructions
==================

Requirements
^^^^^^^^^^^^

* Sphinx version 1.5 or later: http://sphinx-doc.org/contents.html
* LaTeX (and pdflatex, and various LaTeX packages)

On Debian and Ubuntu
^^^^^^^^^^^^^^^^^^^^
::

  # apt-get install python-sphinx texlive texlive-latex-extra libalgorithm-diff-perl \
                    texlive-humanities texlive-generic-recommended texlive-generic-extra

If the version of python-sphinx installed is too old, then an additional
new version can be installed with the Python package installer::

  $ apt-get install python-pip
  $ pip install --user --upgrade Sphinx
  $ export SPHINXBUILD=~/.local/bin/sphinx-build

Export SPHINXBUILD (see above) if Sphinx was installed with pip --user, then follow Make commands below

On Mac OS X
^^^^^^^^^^^

* Install MacTeX_
* Install pip if you do not have it::

  $ sudo easy_install pip

* Install Sphinx::

  $ pip install --user --upgrade Sphinx

.. _MacTeX: http://tug.org/mactex

Make Targets
^^^^^^^^^^^^

To generate PDF::

  $ make latexpdf

To generate hierarchy of HTML pages::

  $ make html

To generate a single HTML page::

  $ make singlehtml

Output goes in `./build` subdirectory.

License
=======

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

A copy of the license is included in the LICENSE_ file.

.. image:: https://i.creativecommons.org/l/by-sa/4.0/88x31.png
   :target: http://creativecommons.org/licenses/by-sa/4.0/
   :alt: Creative Commons License

.. _LICENSE: ./LICENSE

Contributing
============

Master copy of this project is hosted on GitHub:
https://github.com/ARM-software/ebbr

Anyone may contribute to the EBBR project. EBBR discussion uses the
boot-architecture_ and arm.ebbr-discuss mailing lists.
The 'official' list is arm.ebbr-discuss, but the list archives are not
yet public, so boot-architecture_ is being used to keep everything in
the open.

* boot-architechture@lists.linaro.org
* arm.ebbr-discuss@arm.com

Past discussions can be found in the boot-architecture-archive_.

To help track the origin of contributions, this project uses the same
DCO_ "sign-off" process as used by the Linux kernel.
The sign-off is a simple line at the end of the explanation for the
patch, which certifies that you wrote it or otherwise have the right to
pass it on as an open-source patch.  The rules are pretty simple: if you
can certify the below:

Developer's Certificate of Origin 1.1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By making a contribution to this project, I certify that:

        (a) The contribution was created in whole or in part by me and I
            have the right to submit it under the open source license
            indicated in the file; or

        (b) The contribution is based upon previous work that, to the best
            of my knowledge, is covered under an appropriate open source
            license and I have the right under that license to submit that
            work with modifications, whether created in whole or in part
            by me, under the same open source license (unless I am
            permitted to submit under a different license), as indicated
            in the file; or

        (c) The contribution was provided directly to me by some other
            person who certified (a), (b) or (c) and I have not modified
            it.

        (d) I understand and agree that this project and the contribution
            are public and that a record of the contribution (including all
            personal information I submit with it, including my sign-off) is
            maintained indefinitely and may be redistributed consistent with
            this project or the open source license(s) involved.

then you just add a line saying::

        Signed-off-by: Random J Developer <random@developer.example.org>

IRC Channel: ``#ebbr`` on ofct

.. _DCO: https://developercertificate.org/
.. _boot-architecture: https://lists.linaro.org/mailman/listinfo/boot-architecture
.. _boot-architecture-archive: https://lists.linaro.org/pipermail/boot-architecture

Writers Guide
=============

All documentation in this repository uses reStructuredText_ markup
with Sphinx_ extensions.

All files in this project must include the relevant SPDX license identifier
tag. Generally this means each ``.rst`` file should include the line

    ``.. SPDX-License-Identifier: CC-BY-SA-4.0``

.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _Sphinx: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

Original Document
=================
Prior to being relicensed to CC-BY-SA 4.0, this specification was
released by Arm. The original Draft v0.5 text can be found here:

`EBBR Draft v0.5 <https://developer.arm.com/products/architecture/system-architecture/embedded-system-architecture>`_

.. SPDX-License-Identifier: CC-BY-SA-4.0

