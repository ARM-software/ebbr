.. EBBR Source Document
   Copyright Arm Limited, 2017-2019
   Copyright Western Digital Corporation or its affiliates, 2021
   SPDX-License-Identifier: CC-BY-SA-4.0

####################################################
Embedded Base Boot Requirements (EBBR) Specification
####################################################

Copyright © 2017-2019 Arm Limited and Contributors.

Copyright © 2021 Western Digital Corporation or its affiliates, 2021

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

.. image:: images/cc-by-sa-4.0-88x31.*
   :target: http://creativecommons.org/licenses/by-sa/4.0/
   :alt: Creative Commons License
   :align: right

.. tabularcolumns:: l c p{11.5cm}
.. list-table:: Revision History
   :header-rows: 1

   * - Date
     - Issue
     - Changes
   * - 20 Sep 2017
     - 0.51
     - - Confidentiality Change, EBBR version 0.51
   * - 12 Jul 2018
     - 0.6
     - - Relicense to CC-BY-SA 4.0
       - Added Devicetree requirements
       - Added Multiprocessor boot requirements
       - Transitioned to reStructuredText and GitHub
       - Added firmware on shared media requirements
       - RTC is optional
       - Add constraints on sharing devices between firmware and OS
       - Add large note on implementation of runtime modification of
         non-volatile variables
   * - 18 Oct 2018
     - 0.7
     - - Add AArch32 details
       - Refactor Runtime Services text after face to fact meeting at
         Linaro Connect YVR18
   * - 12 Mar 2019
     - 0.8
     - - Update language around SetVariable() and what is available during
         runtime services
       - Editorial changes preparing for v1.0
   * - 31 Mar 2019
     - 1.0
     - - Remove unnecessary UEFI requirements appendix
       - Allow for ACPI vendor id in firmware path
   * - 5 Aug 2020
     - 1.0.1
     - - Update to UEFI 2.8 Errata A
       - Specify UUID for passing DTB
       - Typo and editorial fixes
       - Document the release process
   * - 23 Apr 2021
     - 2.0.0
     - - Reduce the number of UEFI required elements needed for compliance.
       - Add requirement for UpdateCapsule() runtime service.
       - Updated firmware shared storage requirements
       - Refined RTC requirements
       - Fixed ResetSystem() to correctly describe failure condition

.. toctree::
   :numbered:

   chapter1-about
   chapter2-uefi
   chapter3-secureworld
   chapter4-firmware-media
   references
