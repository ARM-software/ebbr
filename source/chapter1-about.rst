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

Comments or change requests can be sent to `boot-architecture@lists.linaro.org`.

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
support embedded platforms, while still preserving the firmware stack that
product vendors are comfortable with.
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

  This document uses Linux as an example but other OS's support EBBR compliant
  systems as well (e.g. FreeBSD, OpenBSD).

- Support multiple architectures

  Any architecture can implement the EBBR requirements.
  Architecture specific requirements will clearly marked as to which
  architecture(s) they apply.

- Design for common embedded hardware

  EBBR support will be implemented on existing developer hardware.
  Generally anything that has a near-upstream U-Boot implementation should be
  able to implement the EBBR requirements.
  EBBR was drafted with readily available hardware in mind, like the
  Raspberry Pi and BeagleBone families of boards, and it is applicable for low cost boards (<$10).

- Plan to evolve over time

  The current release of EBBR is firmly targeted at existing platforms so that
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

This document defines a subset of the boot and runtime services, protocols and
configuration tables defined in the UEFI specification [UEFI]_ that is provided
to an Operating System or hypervisor.

This specification defines the boot and runtime services for a physical system,
including services that are required for virtualization.
It does not define a standardized abstract virtual machine view for a Guest
Operating System.

This specification is referenced by the Arm Base Boot Requirements
Specification [ArmBBR]_ § 4.3.
The UEFI requirements found in this document are similar but not identical to
the requirements found in BBR.
EBBR provides greater flexibility for support embedded designs which cannot
easily meet the stricter BBR requirements.

By definition, all BBR compliant systems are also EBBR compliant, but the
converse is not true.

Conventions Used in this Document
=================================

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in :rfc:`2119`.

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

   AArch32
      Arm 32-bit architectures. AArch32 is a roll up term referring to all
      32-bit versions of the Arm architecture starting at ARMv4.

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
      The lowest Exception level on AArch64. The Exception level that is used to execute
      user applications, in Non-secure state.

   EL1
      Privileged Exception level on AArch64. The Exception level that is used to execute
      Operating Systems, in Non-secure state.

   EL2
      Hypervisor Exception level on AArch64. The Exception level that is used to execute
      hypervisor code. EL2 is always in Non-secure state.

   EL3
      Secure Monitor Exception level on AArch64. The Exception level that is used to
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
