.. SPDX-License-Identifier: CC-BY-SA-4.0

****
UEFI
****

This chapter discusses specific UEFI implementation details for EBBR compliant
platforms.

UEFI Version
============
This document uses version 2.8 Errata A of the UEFI specification [UEFI]_.

UEFI Compliance
===============

EBBR compliant platforms shall conform to the requirements in [UEFI]_ § 2.6,
except where explicit exemptions are provided by this document.

Block device partitioning
-------------------------

The system firmware must implement support for MBR, GPT and El Torito partitioning
on block devices.
System firmware may also implement other partitioning methods as needed by the platform,
but OS support for other methods is outside the scope of this specification.

UEFI System Environment and Configuration
=========================================

The resident UEFI boot-time environment shall use the highest non-secure
privilege level available.
The exact meaning of this is architecture dependent, as detailed below.

Resident UEFI firmware might target a specific privilege level.
In contrast, UEFI Loaded Images, such as third-party drivers and boot
applications, must not contain any built-in assumptions that they are to be
loaded at a given privilege level during boot time since they can, for example,
legitimately be loaded into either EL1 or EL2 on AArch64.

AArch64 Exception Levels
------------------------

On AArch64 UEFI shall execute as 64-bit code at either EL1 or EL2,
depending on whether or not virtualization is available at OS load time.

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

Reserved memory with property no-map [RESMEM]_ in the /reserved-memory
device-tree node shall not be included in the memory map returned by
GetMemoryMap().

Configuration Tables
--------------------

A UEFI system that complies with this specification may provide the additional
tables via the EFI Configuration Table.

Compliant systems are required to provide one, but not both, of the following
tables:

- an Advanced Configuration and Power Interface [ACPI]_ table, or
- a Devicetree [DTSPEC]_ system description

EBBR systems must not provide both ACPI and Devicetree
tables at the same time.
Systems that support both interfaces must provide a configuration
mechanism to select either ACPI or Devicetree,
and must ensure only the selected interface is provided to the OS loader.

Devicetree
^^^^^^^^^^

If firmware provides a Devicetree system description then it must be provided
in Flattened Devicetree Blob (DTB) format version 17 or higher as described in
[DTSPEC]_ § 5.1.
The following GUID must be used in the EFI system table ([UEFI]_ § 4)
to identify the DTB.
The DTB must be contained in memory of type EfiACPIReclaimMemory.
EfiACPIReclaimMemory was chosen to match the recommendation for ACPI
tables which fulfill the same task as the DTB.

.. code-block:: c

    #define EFI_DTB_GUID \
         EFI_GUID(0xb1b621d5, 0xf19c, 0x41a5, \
                  0x83, 0x0b, 0xd9, 0x15, 0x2c, 0x69, 0xaa, 0xe0)

Firmware must have the DTB resident in memory and installed in the EFI system table
before executing any UEFI applications or drivers that are not part of the system
firmware image.
Once the DTB is installed as a configuration table,
the system firmware must not make any modification to it or reference any data
contained within the DTB.

UEFI applications are permitted to modify or replace the loaded DTB.
System firmware must not depend on any data contained within the DTB.
If system firmware makes use of a DTB for its own configuration,
it should use a separate private copy that is not installed in the
EFI System Table or otherwise be exposed to EFI applications.

UEFI Secure Boot (Optional)
---------------------------

UEFI Secure Boot is optional for this specification.

If Secure Boot is implemented, it must conform to the UEFI specification for Secure Boot. There are no additional
requirements for Secure Boot.

UEFI Runtime Services
=====================

UEFI runtime services exist after the call to ExitBootServices() and are
designed to provide a limited set of persistent services to the platform
Operating System or hypervisor.
Functions contained in EFI_RUNTIME_SERVICES are expected to be available
during both boot services and runtime services.
However, it isn't always practical for all EFI_RUNTIME_SERVICES functions
to be callable during runtime services due to hardware limitations.
If any EFI_RUNTIME_SERVICES functions are only available during boot services
then firmware shall provide the `EFI_RT_PROPERTIES_TABLE` to
indicate which functions are available during runtime services.
Functions that are not available during runtime services shall return
EFI_UNSUPPORTED.

:numref:`uefi_runtime_service_requirements` details which EFI_RUNTIME_SERVICES
are required to be implemented during boot services and runtime services.

.. _uefi_runtime_service_requirements:
.. table:: EFI_RUNTIME_SERVICES Implementation Requirements

   ============================== ============= ================
   EFI_RUNTIME_SERVICES function  Boot Services Runtime Services
   ============================== ============= ================
   EFI_GET_TIME                   Optional      Optional
   EFI_SET_TIME                   Optional      Optional
   EFI_GET_WAKEUP_TIME            Optional      Optional
   EFI_SET_WAKEUP_TIME            Optional      Optional
   EFI_SET_VIRTUAL_ADDRESS_MAP    N/A           Required
   EFI_CONVERT_POINTER            N/A           Required
   EFI_GET_VARIABLE               Required      Optional
   EFI_GET_NEXT_VARIABLE_NAME     Required      Optional
   EFI_SET_VARIABLE               Required      Optional
   EFI_GET_NEXT_HIGH_MONO_COUNT   N/A           Optional
   EFI_RESET_SYSTEM               Required      Optional
   EFI_UPDATE_CAPSULE             Optional      Optional
   EFI_QUERY_CAPSULE_CAPABILITIES Optional      Optional
   EFI_QUERY_VARIABLE_INFO        Optional      Optional
   ============================== ============= ================

Runtime Device Mappings
-----------------------

Firmware shall not create runtime mappings, or perform any runtime IO that will
conflict with device access by the OS.
Normally this means a device may be controlled by firmware, or controlled by
the OS, but not both.
E.g. if firmware attempts to access an eMMC device at runtime then it will
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

If firmware does not support access to the RTC, then GetTime() and
SetTime() shall return EFI_UNSUPPORTED,
and the OS must use a device driver to control the RTC.

UEFI Reset and Shutdown
-----------------------

ResetSystem() is required to be implemented in boot services, but it is
optional for runtime services.
During runtime services, the operating system should first attempt to
use ResetSystem() to reset the system.
If firmware doesn't support ResetSystem() during runtime services,
then the call will immediately return EFI_UNSUPPORTED, and the OS should
fall back to an architecture or platform specific reset mechanism.

On AArch64 platforms implementing [PSCI]_,
if ResetSystem() is not implemented then the Operating System should fall
back to making a PSCI call to reset or shutdown the system.

Runtime Variable Access
-----------------------

There are many platforms where it is difficult to implement SetVariable() for
non-volatile variables during runtime services because the firmware cannot
access storage after ExitBootServices() is called.

e.g., If firmware accesses an eMMC device directly at runtime, it will
collide with transactions initiated by the OS.
Neither U-Boot nor Tianocore have a generic solution for accessing or updating
variables stored on shared media. [#OPTEESupplicant]_

If a platform does not implement modifying non-volatile variables with
SetVariable() after ExitBootServices(),
then firmware shall return EFI_UNSUPPORTED for any call to SetVariable(),
and must advertise that SetVariable() isn't available during runtime services
via the `RuntimeServicesSupported` value in the `EFI_RT_PROPERTIES_TABLE`
as defined in [UEFI]_ § 4.6.
EFI applications can read `RuntimeServicesSupported` to determine if calls
to SetVariable() need to be performed before calling ExitBootServices().

Even when SetVariable() is not supported during runtime services, firmware
should cache variable names and values in EfiRuntimeServicesData memory so
that GetVariable() and GetNextVeriableName() can behave as specified.

.. [#OPTEESupplicant] It is worth noting that OP-TEE has a similar problem
   regarding secure storage.
   OP-TEE's chosen solution is to rely on an OS supplicant agent to perform
   storage operations on behalf of OP-TEE.
   The same solution may be applicable to solving the UEFI non-volatile
   variable problem, but it requires additional OS support to work.
   Regardless, EBBR compliance does not require SetVariable() support
   during runtime services.

   https://optee.readthedocs.io/en/latest/architecture/secure_storage.html
