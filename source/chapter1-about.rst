.. SPDX-License-Identifier: CC-BY-SA-4.0

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
For example, an Arm A-class embedded platform will benefit
from a standard interface that supports features such as secure boot and
firmware update.

This specification defines the base firmware requirements for EBBR compliant platforms.
The requirements in this specification are expected to be minimal yet complete,
while leaving plenty of room for innovations and design details.
This specification is intended to be OS-neutral.

It leverages the prevalent industry standard firmware specification of [UEFI]_.

Comments or change requests can be sent to arm.ebbr-discuss@arm.com.

Guiding Principles
==================

EBBR as a specification defines requirements on platforms and operating systems,
but requirements alone don't provide insight into why the specification is
written the way it is, or what problems it is intended to solve.
Using the assumption that better understanding of the thought process behind
EBBR will result in better implementations, this section is a discussion of the
goals and guiding principle that shaped EBBR.

This section should be considered commentary, and not a formal part of the specification.

EBBR was written as a response to the lack of boot sequence standardization in the embedded system ecosystem.
As embedded systems are becoming more sophisticated and connected,
it is becoming increasingly important for embedded systems to run standard OS
distributions and software stacks, or to have consistent behaviour across a
large deployment of heterogeneous platforms.
However, the lack of consistency between platforms often requires per-platform
customization to get an OS image to boot on multiple platforms.

A large part of this ecosystem is based on U-Boot and Linux.
Vendors have heavy investments in both projects and are not interested in large
scale changes to their firmware architecture.
The challenge for EBBR is to define a set of boot standards that reduce the
amount of custom engineering required, make it possible for OS distributions to
support embedded platforms, while still preserving the firmware stack product
vendors are comfortable with.
Or in simpler terms, EBBR is designed to solve the embedded boot mess by
adding a defined standard (UEFI) to the existing firmware projects (U-Boot).

However, EBBR is a specification, not an implementation.
The goal of EBBR is not to mandate U-Boot and Linux.
Rather, it is to mandate interfaces that can be implemented by any firmware or
OS project, while at the same time work with both Tianocore/EDK2 and U-Boot to
ensure that the EBBR requirements are implemented by both projects.
[#EDK2Note]_

.. [#EDK2Note] Tianocore/EDK2 and U-Boot are highlighted here because at the
   time of writing these are the two most important firmware projects that
   implement UEFI.
   Tianocore/EDK2 is a full featured UEFI implementation and so should
   automatically be EBBR compliant.
   U-Boot is the incumbant firmware project for embedded platforms and has
   steadily been adding UEFI compliance since 2016.

The following guiding principles are used while developing the EBBR specification.

- Be agnostic about ACPI and Devicetree.

  EBBR explicitly does not require a specific system description language.
  Both Devicetree and ACPI are supported.
  The Linux kernel supports both equally well, and so EBBR doesn't require one
  over the other.
  However, EBBR does require the system description to be supplied by the
  platform, not the OS.
  The platform must also conform to the relevant ACPI or DT specifications and
  adhere to platform compatibility rules. [#CompatRules]_

.. [#CompatRules] It must be acknowledged that at the time of writing this
   document, platform compatibility rules for DT platforms are not well defined
   or documented.
   We the authors recognize that this is a problem and are working to solve it
   in parallel with this specification.

- Focus on the UEFI interface, not a specific codebase

  EBBR does not require a specific firmware implementation.
  Any firmware project can implement these interfaces.
  Neither U-Boot nor Tianocore/EDK2 are required.

- Design to be implementable and useful today

  The drafting process for EBBR worked closely with U-Boot and Tianocore
  developers to ensure that current upstream code will meet the requirements.

- Design to be OS independent

  This document uses Linux as an example but other OS's are expected.

- Support multiple architectures

  Any architecture can implement the EBBR requirements.

  .. note::
     At the time of writing this document only addresses AArch64, but AArch32 and others architectures are expected.

- Design for common embedded hardware

  EBBR support will be implemented on existing developer hardware.
  Generally anything that has a near-upstream U-Boot implementation should be
  able to implement the EBBR requirements.
  EBBR was drafted with readily available hardware in mind, like the
  Raspberry Pi and BeagleBone families of boards, and it is applicable for low cost boards (<$10).

- Design to support automated testing

  EBBR support can provide methods to make it easier and more reliable to
  automate the boot sequence of embedded devices.

  * All identifiers used within the boot process need to be unique
    across devices, persistent across reboots and firmware updates.
    e.g. serial numbers, MAC addresses, USB device ID's.

  * Behaviour and the output need to be consistent, so that the same
    action or error produces the same output from one boot to the next.

  * Automation will rely on a serial console, not graphical. Support for
    automation means providing a reliable serial console even if the
    primary console is intended to be graphical. Serial console can be
    enabled via jumpers or persistent software configuration.

  * Provide clear version information in the output of every boot

  * Provide clear status messages for critical stages within boot to assist
    in triage when boot is reported as "failed".

  * Provide clear error messages for all supported error conditions and
    failures.

  * Use a consistent format, without colour code or escape characters, for
    all messages, errors and warnings:

    * Version strings::

       [BOOT] Version: <version>\n

    * Status messages::

       [BOOT] Starting kernel ...\n

    * Warnings::

       [WARN] Unable to find <file>\n

- Plan to evolve over time

  The v1.0 release of EBBR is firmly targeted at existing platforms so that
  gaining EBBR compliance may require a firmware update, but will not require
  hardware changes for the majority of platforms.

  Future EBBR releases will tighten requirements to add features and improve
  compatibility, which may affect hardware design choices.
  However, EBBR will not retroactively revoke support from previously compliant
  platforms.
  Instead, new requirements will be clearly documented as being over and above
  what was required by a previous release.
  Existing platforms will be able to retain compliance with a previous
  requirement level.
  In turn, OS projects and end users can choose what level of EBBR compliance
  is required for their use case.

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
operating system.
SBBR is targeted at the server ecosystem and places strict requirements on the
platform to ensure cross vendor interoperability.
EBBR on the other hand allows more flexibility to support embedded designs
which do not fit within the SBBR model.
For example, a platform that isn't SBBR compliant because the SoC is only
supported using Devicetree could be EBBR compliant, but not SBBR compliant.

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
