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

The documentation in this project is provided under the terms of the
Creative Commons Attribution Share-Alike License.
Licensing details can be found in the LICENSE.rst_ file.

.. _LICENSE.rst: ./LICENSE.rst

Contributing
============

Master copy of this project is hosted on GitHub:
https://github.com/ARM-software/ebbr

Anyone may contribute to EBBR. Contributions must be made with a
Developer Certificate of Origin (DCO_) attestation that the contribution
confirms to the license of the project. The attestation is made by the
developer including a ``Signed-off-by: <email-address>`` tag in the
commit text of the contribution.

.. _DCO: https://developercertificate.org/

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

