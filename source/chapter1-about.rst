*******************
About This Document
*******************

Introduction
============

This Embedded Base Boot Requirements (EBBR) specification defines an interface
between platform firmware and an operating system that is suitable for embedded
platforms.
EBBR compliant platforms present a consistent interface that will boot an EBBR
compliant operating system without any custom tailoring required.
For example, an Arm A-class embedded networking platform will benefit
from a standard interface that supports features such as secure boot and
firmware update.

This specification defines the base firmware requirements for EBBR compliant platforms.
The requirements in this specification are expected to be minimal yet complete,
while leaving plenty of room for innovations and design details.
This specification is intended to be OS-neutral.

It leverages the prevalent industry standard firmware specification of [UEFI]_.

Comments or change requests can be sent to arm.ebbr-discuss@arm.com.

Scope
=====
This document defines the boot and runtime services that are expected by an
Operating System or hypervisor, for an Arm embedded device, which follows the
UEFI specification [UEFI]_.

This specification defines the boot and runtime services for a physical system,
including services that are required for virtualization.
It does not define a standardized abstract virtual machine view for a Guest
Operating System.

This specification is similar to the Arm Server Base Boot Requirements
specification [SBBR]_ in that it defines the firmware interface presented to an
operating system, with SBBR having stricter requirements on hardware and
firmware than EBBR.
EBBR allows for design decisions that are common in the embedded space, but not
supported by the server ecosystem.
For example, an embedded system may use a single eMMC storage device to hold
both firmware and operating system images.
By definition, all SBBR compliant systems are also EBBR compliant, but the
converse is not true.

Cross References
================
This document cross-references sources that are listed in the References
section by using the section sign §.

Examples:

UEFI § 6.1 - Reference to the UEFI specification [UEFI]_ section 6.1

Terms and abbreviations
=======================

This document uses the following terms and abbreviations.

.. glossary::

   A64
      The 64-bit Arm instruction set used in AArch64 state.
      All A64 instructions are 32 bits.

   AArch64 state
      The Arm 64-bit Execution state that uses 64-bit general purpose
      registers, and a 64-bit program counter (PC), Stack Pointer (SP), and
      exception link registers (ELR).

   AArch64
      Execution state provides a single instruction set, A64.

   EFI Loaded Image
      An executable image to be run under the UEFI environment,
      and which uses boot time services.

   EL0
      The lowest Exception level. The Exception level that is used to execute
      user applications, in Non-secure state.

   EL1
      Privileged Exception level. The Exception level that is used to execute
      Operating Systems, in Non-secure state.

   EL2
      Hypervisor Exception level. The Exception level that is used to execute
      hypervisor code. EL2 is always in Non-secure state.

   EL3
      Secure Monitor Exception level. The Exception level that is used to
      execute Secure Monitor code, which handles the transitions between
      Non-secure and Secure states.  EL3 is always in Secure state.

   Logical Unit (LU)
      A logical unit (LU) is an externally addressable, independent entity
      within a device. In the context of storage, a single device may use
      logical units to provide multiple independent storage areas.

   OEM
      Original Equipment Manufacturer. In this document, the final device
      manufacturer.

   SiP
      Silicon Partner. In this document, the silicon manufacturer.

   UEFI
      Unified Extensible Firmware Interface.

   UEFI Boot Services
      Functionality that is provided to UEFI Loaded Images during the UEFI boot
      process.

   UEFI Runtime Services
      Functionality that is provided to an Operating System after the
      ExitBootServices() call.
