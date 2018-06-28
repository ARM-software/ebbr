****
UEFI
****

UEFI Version
============

Boot and system firmware for Arm embedded devices can be based on the UEFI
specification [UEFI]_, version 2.7 or later, incorporating the AArch64 bindings.

UEFI Compliance
===============

Any UEFI-compliant system must follow the requirements that are laid out in
section 2.6 of the UEFI specification [UEFI]_.
However, to ensure a common boot architecture for embedded-class, systems
compliant with this specification must always provide the UEFI services and
protocols that are listed in Appendix A, Appendix B, and Appendix C of this
document.

UEFI System Environment and Configuration
=========================================

AArch64 Exception Levels
------------------------

The resident AArch64 UEFI boot-time environment is specified to "Use the
highest 64-bit Non-secure privilege level available".
This level is either EL1 or EL2, depending on whether or not virtualization is
used or supported.

Resident UEFI firmware might target a specific Exception level.
In contrast, UEFI Loaded Images, such as thirdparty drivers and boot
applications, must not contain any built-in assumptions that they are to be
loaded at a given Exception level during boot time, since they can legitimately
be loaded into EL1 or EL2.

UEFI Boot at EL2
^^^^^^^^^^^^^^^^

Most systems are expected to boot UEFI at EL2, to allow for the installation of
a hypervisor or a virtualization aware Operating System.

UEFI Boot at EL1
^^^^^^^^^^^^^^^^

Booting of UEFI at EL1 is most likely within a hypervisor hosted Guest
Operating System environment, to allow the subsequent booting of a
UEFI-compliant Operating System.
In this instance, the UEFI boot-time environment can be provided, as a
virtualized service, by the hypervisor and not as part of the host firmware.

System Volume Format
--------------------

The system firmware must support all partitioning standards required
by the UEFI specification.

On systems where the system firmware binaries reside on the System Volume then
the System Volume must be pre-configured with a partition table and include
protective partitions to reduce risk of accidental destruction of the system
firmware.

All pre-installed partition tables must use GPT partitioning unless
some immutable feature of the platform (such as a mask programmed boot ROM)
makes this impossible; on such platforms MBR partitioning may be
used as an alternative.

GPT partitioning
^^^^^^^^^^^^^^^^

Any pre-installed partition table must strictly conform to the UEFI
specification and include a protective MBR authored exactly as
described in UEFI specification (hybrid partitioning schemes are not
permitted).

Pre-installed protective partitions must have the Platform Required
Attribute Flag set.

It is recommended that automatic system disk partitioning utilities
preserve Platform Required partitions as is, and that manual disk
partitioning utilities provide warnings and/or other safe guards to
reduce risk of accidental removal.

MBR partitioning
^^^^^^^^^^^^^^^^

Pre-installed protective partitions should have a partition type of 0xF8
unless some immutable feature of the platform makes this impossible.

It is recommended that disk partitioning utilities treat such
partitions in the same manner as GPT partitions with the Platform
Required Attribute Flag set.

It is recommended that pre-installed protective partitions that are not
type 0xF8 be located wholly within 1MB of the start of the disk.

Automatic disk partitioning utilities shall not create partitions
within 1MB of the start of the disk. Manual disk partitioning
utilities should avoid recommending that partitions start within
1MB of the start of the disk.

UEFI Boot Services
==================

Memory Map
----------

The UEFI environment must provide a system memory map, which must include all
appropriate devices and memories that are required for booting and system
configuration.

All RAM defined by the UEFI memory map must be identity-mapped, which means
that virtual addresses must equal physical addresses.

The default RAM allocated attribute must be EFI_MEMORY_WB.

UEFI Loaded Images
------------------

UEFI loaded images for AArch64 must be in 64-bit PE/COFF format and must
contain only A64 code.

Configuration Tables
--------------------

A UEFI system that complies with this specification may provide the additional
tables via the EFI Configuration Table.

Compliant systems are required to provide one, but not both, of the following
tables.

- An Advanced Configuration and Power Interface [ACPI]_ table, or
- a Devicetree [DTSPEC]_ system description

As stated above, EBBR systems must not provide both ACPI and Devicetree
tables at the same time.
Systems that support both interfaces must provide a configuration
mechanism to select either ACPI or Devicetree,
and must ensure only the selected interface is provided to the OS loader.

UEFI Secure Boot (Optional)
---------------------------

UEFI Secure Boot is optional for this specification.

If Secure Boot is implemented, it must conform to the UEFI specification for Secure Boot. There are no additional
requirements for Secure Boot.

UEFI Runtime Services
=====================

UEFI Runtime Services exist after the call to ExitBootServices() and are
designed to provide a limited set of persistent services to the platform
Operating System or hypervisor.

The Runtime Services that are listed in Appendix B must be provided.

Runtime Exception Level
-----------------------

UEFI 2.7 enables runtime services to be supported at either EL1 or EL2, with
appropriate virtual address mappings.
When called, subsequent runtime service calls must be from the same Exception
level.

Runtime Memory Map
------------------

Before calling ExitBootServices(), the final call to GetMemoryMap() returns a
description of the entire UEFI memory map, that includes the persistent Runtime
Services mappings.

After the call to ExitBootServices(), the Runtime Services page mappings can be
relocated in virtual address space by calling SetVirtualAddressMap().
This call allows the Runtime Services to assign virtual addresses that are
compatible with the incoming Operating System memory map.

A UEFI runtime environment compliant with this specification must not be
written with any assumption of an identity mapping between virtual and physical
memory maps.

UEFI operates with a 4K page size. With Runtime Services, these pages are
mapped into the Operating System address space.

To allow Operating Systems to use 64K page mappings, UEFI 2.7, constrains all
mapped 4K memory pages to have identical page attributes, within the same
physical 64K page.

Real-time Clock
---------------

The Real-time Clock must be accessible via the UEFI runtime firmware, and the
following services must be provided:

- GetTime()
- SetTime()

It is permissible for SetTime() to return an error on systems where the
Real-time Clock cannot be set by this call.

UEFI Reset and Shutdown
-----------------------

The UEFI Runtime service ResetSystem() must implement the following commands,
for purposes of power management and system control.

- EfiResetCold()
- EfiResetShutdown()
  * EfiResetShutdown must not reboot the system.

If firmware updates are supported through the Runtime Service of
UpdateCapsule(), then ResetSystem() might need to support the following
command:

- EfiWarmReset()

.. note:: On platforms implementing the Power State Coordination Interface
   specification [PSCI]_, it is still required that EBBR compliant
   Operating Systems calls to reset the system will go via Runtime Services
   and not directly to PSCI.

Set Variable
------------

Non-volatile UEFI variables must persist across reset, and emulated variables
in RAM are not permitted.
The UEFI Runtime Services must be able to update the variables directly without
the aid of the Operating System.

.. note:: This normally requires dedicated storage for UEFI variables that is
   not directly accessible from the Operating System.