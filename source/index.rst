.. EBBR Source Document
   Copyright Arm Limited, 2017-2019
   SPDX-License-Identifier: CC-BY-SA-4.0

####################################################
Embedded Base Boot Requirements (EBBR) Specification
####################################################

Copyright © 2017-2019 Arm Limited and Contributors.

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

.. image:: images/cc-by-sa-4.0-88x31.*
   :target: http://creativecommons.org/licenses/by-sa/4.0/
   :alt: Creative Commons License
   :align: right

.. tabularcolumns:: l c p{11.5cm}
.. table:: Revision History

   ================= ========= =============================================
   Date              Issue     Changes
   ================= ========= =============================================
   20 September 2017 0.51      Confidentiality Change, EBBR version 0.51
   6 July 2018       0.6-pre1  - Relicense to CC-BY-SA 4.0
                               - Added Devicetree requirements
                               - Added Multiprocessor boot requirements
                               - Transitioned to reStructuredText and GitHub
                               - Added firmware on shared media requirements
                               - RTC is optional
                               - Add constraints on sharing devices between
                                 firmware and OS
   12 July 2018      0.6       - Response to comments on v0.6-pre1
                               - Add large note on implementation of runtime
                                 modification of non-volatile variables
   18 October 2018   0.7       - Add AArch32 details
                               - Refactor Runtime Services text after face
                                 to fact meeting at Linaro Connect YVR18
   12 March 2019     0.8       - Update language around SetVariable() and
                                 what is available during runtime services
                               - Editorial changes preparing for v1.0
   ================= ========= =============================================

.. toctree::
   :numbered:

   chapter1-about
   chapter2-uefi
   chapter3-secureworld
   chapter4-firmware-media
   appendix-a-uefi-features
   references
