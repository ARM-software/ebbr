.. SPDX-License-Identifier: CC-BY-SA-4.0

****
UEFI
****

This chapter discusses specific UEFI implementation details for EBBR compliant
platforms.

UEFI Version
============
This document uses version 2.7 of the UEFI specification [UEFI]_.

UEFI Compliance
===============

EBBR compliant platforms shall conform to the requirements in [UEFI]_ § 2.6,
except where explicit exemptions are provided by this document.

EBBR compliant platforms shall also implement the UEFI services and
protocols that are listed in :ref:`appendix-uefi-requirements` of this
document.

Block device partitioning
-------------------------

The system firmware must implement support for MBR, GPT and El Torito partitioning.

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

The Runtime Services that are listed in :ref:`appendix-uefi-required-runtime`
must be provided.

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

Runtime Device Mappings
-----------------------

Firmware shall not create runtime mappings, or perform any runtime IO that will
conflict with device access by the OS.
Normally this means a device may be controlled by firmware, or controlled by
the OS, but not both.
e.g. If firmware attempts to access an eMMC device at runtime then it will
conflict with transactions being performed by the OS.

Devices that are provided to the OS (i.e., via PCIe discovery or ACPI/DT
description) shall not be accessed by firmware at runtime.
Similarly, devices retained by firmware (i.e., not discoverable by the OS)
shall not be accessed by the OS.

Only devices that explicitly support concurrent access by both firmware and an
OS may be mapped at runtime by both firmware and the OS.

Real-time Clock (RTC)
^^^^^^^^^^^^^^^^^^^^^

Not all embedded systems include an RTC, and even if one is present,
it may not be possible to access the RTC from runtime services.
e.g., The RTC may be on a shared I2C bus which runtime services cannot access
because it will conflict with the OS.

Firmware still must provide the UEFI GetTime() and SetTime() runtime service
calls, but if an RTC isn't present, or cannot be accessed at runtime, then both
calls shall return EFI_DEVICE_ERROR.

UEFI Reset and Shutdown
-----------------------

The UEFI Runtime service ResetSystem() must implement the following commands,
for purposes of power management and system control.

- EfiResetCold()
- EfiResetShutdown()
  * EfiResetShutdown must not reboot the system.

The UEFI Runtime service ResetSystem() must output stable, reliable and
unique messages for all supportable error conditions and failures, including
resets::

 [UEFI] Resetting CPU ....\n

If firmware updates are supported through the Runtime Service of
UpdateCapsule(), then ResetSystem() might need to support the following
command:

- EfiWarmReset()

.. note:: On platforms implementing the Power State Coordination Interface
   specification [PSCI]_, it is still required that EBBR compliant
   Operating Systems calls to reset the system will go via Runtime Services
   and not directly to PSCI.

::

 [UEFI] Warm Reset of CPU ....\n

Runtime Variable Access
-----------------------

.. todo::

   There are many platforms where it is difficult to support SetVariable() for
   non-volatile variables because the firmware cannot access storage after
   ExitBootServices() is called.
   e.g., If firmware accesses an eMMC device directly at runtime, it will
   collide with transactions initiated by the OS.
   Neither U-Boot nor Tianocore have a solution for accessing shared media for
   variable updates. [#OPTEESupplicant]_

   In these platforms SetVariable() calls with the EFI_VARIABLE_NON_VOLATILE
   attribute set will work in boot services, but will fail in runtime services.
   The [UEFI]_ specification doesn't address what to do in this situation.
   We need feedback on options before writing this section of EBBR, or making a
   proposal to modify UEFI.

   We need a solution that communicates to the OS that non-volatile variable
   updates are not supported at runtime, and that defines the behaviour when
   SetVariable() is called with the EFI_VARIABLE_NON_VOLATILE attribute.

   Presumably, the solution will require SetVariable() to return
   EFI_INVALID_PARAMETER if called with the EFI_VARIABLE_NON_VOLATILE
   attribute, but beyond that there are a number of options:

   #. Clear EFI_VARIABLE_NON_VOLATILE from all variables at ExitBootServices()

      If the platform is incapable of updating non-volatile variables from Runtime
      Services then it must clear the EFI_VARIABLE_NON_VOLATILE attribute from all
      non-volatile variables when ExitBootServices() is called.

      An OS can discover that non-volatile variables cannot be updated at
      runtime by noticing that the NON_VOLATILE attribute is not set.

   #. Clear all variables at ExitBootServices()

      If the platform is incapable of updating non-volatile variables from Runtime
      Services then it will clear all variables and return EFI_INVALID_PARAMETER
      on all calls to SetVariable().

      SUSE in particular currently uses this behaviour to decide whether or not
      to treat the ESP as removable media.

   #. Advertise that SetVariable() doesn't work at runtime with another variable

      Platforms can check another variable to determine if they have this quirk,
      perhaps by adding a new BootOptionSupport flag.

   This is not a complete list, and other options can still be proposed. We're
   looking for feedback on what would be most faithful to the UEFI spec, and
   would work for the OS distributions before filling out this section of the
   specification.

   Comments can be sent to the boot-architecture@lists.linaro.org mailing list.

.. [#OPTEESupplicant] It is worth noting that OP-TEE has a similar problem
   regarding secure storage.
   OP-TEE's chosen solution is to rely on an OS supplicant agent to perform
   storage operations on behalf of OP-TEE.
   The same solution may be applicable to solving the UEFI non-volatile
   variable problem, but that approach is also not entirely UEFI compliant
   because it requires additional OS support to work.

   https://github.com/OP-TEE/optee_os/blob/master/documentation/secure_storage.md
