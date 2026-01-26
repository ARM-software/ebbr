.. EBBR Source Document
   Copyright Arm Limited, 2017-2026
   Copyright Western Digital Corporation or its affiliates, 2021
   SPDX-License-Identifier: CC-BY-SA-4.0

####################################################
Embedded Base Boot Requirements (EBBR) Specification
####################################################

Copyright © 2017-2026 Arm Limited and Contributors.

Copyright © 2021 Western Digital Corporation or its affiliates.

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
https://creativecommons.org/licenses/by-sa/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

.. image:: images/cc-by-sa-4.0-88x31.*
   :target: https://creativecommons.org/licenses/by-sa/4.0/
   :alt: Creative Commons License
   :align: right

.. list-table:: Revision History
   :widths: 15 10 75
   :header-rows: 1
   :class: longtable

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
     - - Update language around `SetVariable()` and what is available during
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
       - Add requirement for `UpdateCapsule()` runtime service.
       - Updated firmware shared storage requirements
       - Refined RTC requirements
       - Fixed `ResetSystem()` to correctly describe failure condition
   * - 6 Aug 2021
     - 2.0.1
     - - Update UEFI version to 2.9
       - Update Devicetree spec version to v0.3
       - Add RISC-V platform text
       - Temporarily drop ESRT requirement
       - Fix typos
   * - 7 Dec 2022
     - 2.1.0
     - - Restore ESRT requirement when capsule update is implemented
       - Update UEFI version to 2.10
       - Add an EFI Conformance Profile for EBBR v2.1.x
       - Drop requirement on now-ignored RISC-V boot-hartid and add
         `RISCV_EFI_BOOT_PROTOCOL` requirement
       - Update ACPI version to 6.4
       - Update PSCI version to issue D.b (v1.1)
       - Update BBR version to issue G (v2.0)
       - Add DTB requirements
       - Fix typos and spelling
       - Refresh links
   * - 5 Jun 2024
     - 2.2.0
     - - Require capsule update "on disk" and variables
       - Require the TCG2 protocol if system has a TPM
       - Define a file format for storing EFI variables
       - Provision conformance profile 2.2 guid
       - Recommend the firmware update protocol, PSCI >= 1.0, SMCCC >= 1.1
       - Make monotonic counter optional
       - Clarify that ConnectController must be implemented
       - Bump ACPI, PSCI and Devicetree references versions, refresh reference
         for RISC-V hypervisor extension, mention dt-schema
       - Links refresh and additions, typos and syntax fixes, cosmetic changes,
         formatting conventions, notes movements, chapters changes, glossary
         adjustments
   * - 20 Dec 2024
     - 2.3.0
     - - Formalize the Boot Manager requirements
       - Require authenticated FMP capsules for firmware update
       - Deprecate spin tables for AArch64
       - Add conformance profile GUID for version 2.3
       - Remove ambiguities around the collation protocol
       - Bump referenced versions: UEFI to v2.11, PSCI to v1.3, SMCCC to 1.6 G,
         BBR to v2.1 and dt-schema to v2024.09
       - Move some footnotes around
   * - 17 Dec 2025
     - 2.4.0-pre1
     - - Recommend the EFI Graphics Output Protocol
       - Split AArch64 requirements section § 3.2, add conditional requirements
         on FF-A, PFDI and SCMI, recommend SOC_ID and TRNG, warn about future
         PSCI & SMCCC versions requirements, simplify PSCI wording, add a note
         on SMCCC conduit
       - Raise RISC-V SBI requirement and rename section § 3.3
       - Refer to semantic versioning, clarify backward compatibility and remove
         the mention of levels completely
       - Add conformance profile GUID for version 2.4
       - Update references and links, bump referenced versions of ACPI, BBR,
         dt-schema and SMCCC, add references to FF-A, PFDI, SCMI, semantic
         versioning and TRNG, remove reference to the RISC-V platform
         specification
       - Formatting changes and cosmetic adjustments

.. toctree::
   :numbered:

   chapter1-about
   chapter2-uefi
   chapter3-secureworld
   chapter4-firmware-media
   chapter5-variable-storage
   references
