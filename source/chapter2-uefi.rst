.. SPDX-License-Identifier: CC-BY-SA-4.0

****
UEFI
****

This chapter discusses specific UEFI implementation details for EBBR compliant
platforms.

UEFI Version
============

This document uses version 2.10 of the UEFI specification [UEFI]_.

UEFI Compliance
===============

EBBR compliant platform shall conform to a subset of the [UEFI]_ spec as listed
in this section.
Normally, UEFI compliance would require full compliance with all items listed
in :UEFI:`2.6`.
However, the EBBR target market has a reduced set of requirements,
and so some UEFI features are omitted as unnecessary.

Required Elements
-----------------

This section replaces the list of required elements in :UEFI:`2.6.1`.
All of the following UEFI elements are required for EBBR compliance.

.. list-table:: UEFI Required Elements
   :widths: 50 50
   :header-rows: 1

   * - Element
     - Requirement
   * - `EFI_SYSTEM_TABLE`
     - The system table is required to provide access to UEFI Boot Services,
       UEFI Runtime Services, consoles, and other firmware, vendor and platform
       information.
   * - `EFI_BOOT_SERVICES`
     - All functions defined as boot services must exist.
       Methods for unsupported or unimplemented behaviour must return
       an appropriate error code.
   * - `EFI_RUNTIME_SERVICES`
     - All functions defined as runtime services must exist.
       Methods for unsupported or unimplemented behaviour must return
       an appropriate error code.
       If any runtime service is unimplemented, it must be indicated
       via the `EFI_RT_PROPERTIES_TABLE`.
   * - `EFI_LOADED_IMAGE_PROTOCOL`
     - Must be installed for each loaded image.
   * - `EFI_LOADED_IMAGE_DEVICE_PATH_PROTOCOL`
     - Must be installed for each loaded image.
   * - `EFI_DEVICE_PATH_PROTOCOL`
     - An `EFI_DEVICE_PATH_PROTOCOL` must be installed onto all device
       handles provided by the firmware.
   * - `EFI_DEVICE_PATH_UTILITIES_PROTOCOL`
     - Interface for creating and manipulating UEFI device paths.

.. list-table:: Notable omissions from :UEFI:`2.6.1`
   :widths: 50 50
   :header-rows: 1

   * - Element
     - Note
   * - `EFI_DECOMPRESS_PROTOCOL`
     - Native EFI decompression is rarely used and therefore not required.

Required Platform Specific Elements
-----------------------------------

This section replaces the list of required elements in :UEFI:`2.6.2`.
All of the following UEFI elements are required for EBBR compliance.

.. list-table:: UEFI Platform-Specific Required Elements
   :widths: 50 50
   :header-rows: 1

   * - Element
     - Description
   * - Console devices
     - The platform must have at least one console device.
   * - `EFI_SIMPLE_TEXT_INPUT_PROTOCOL`
     - Needed for console input.
   * - `EFI_SIMPLE_TEXT_INPUT_EX_PROTOCOL`
     - Needed for console input.
   * - `EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL`
     - Needed for console output.
   * - `EFI_DEVICE_PATH_TO_TEXT_PROTOCOL`
     - Needed for console output.
   * - `EFI_HII_STRING_PROTOCOL`
     - Required by EFI shell and for compliance testing.
   * - `EFI_HII_DATABASE_PROTOCOL`
     - Required by EFI shell and for compliance testing.
   * - `EFI_UNICODE_COLLATION2_PROTOCOL`
     - Required by EFI shell and for compliance testing.
   * - `EFI_BLOCK_IO_PROTOCOL`
     - Required for block device access.
   * - `EFI_SIMPLE_FILE_SYSTEM_PROTOCOL`
     - Required if booting from block device is supported.
   * - `EFI_RNG_PROTOCOL`
     - Required if the platform has a hardware entropy source.
   * - `EFI_SIMPLE_NETWORK_PROTOCOL`
     - Required if the platform has a network device.
   * - HTTP Boot
     - Required if the platform supports network booting. (:UEFI:`24.7`)
   * - `RISCV_EFI_BOOT_PROTOCOL`
     - Required on RISC-V platforms. (:UEFI:`2.3.7.1` and [RVUEFI]_)

The following table is a list of notable deviations from :UEFI:`2.6.2`.
Many of these deviations are because the EBBR use cases do not require
interface specific UEFI protocols, and so they have been made optional.

.. list-table:: Notable Deviations from :UEFI:`2.6.2`
   :widths: 50 50
   :header-rows: 1

   * - Element
     - Description of deviation
   * - `LoadImage()`
     - The `LoadImage()` boot service is not required to install an
       `EFI_HII_PACKAGE_LIST_PROTOCOL` for an image containing a custom PE/COFF
       resource with the type 'HII'. HII resource images are not needed to run
       the UEFI shell or the SCT.
   * - `ConnectController()`
     - The `ConnectController()` boot service is not required to support the
       `EFI_PLATFORM_DRIVER_OVERRIDE_PROTOCOL`,
       `EFI_DRIVER_FAMILY_OVERRIDE_PROTOCOL`, and
       `EFI_BUS_SPECIFIC_DRIVER_OVERRIDE_PROTOCOL`.
       These override protocols are
       only useful if drivers are loaded as EFI binaries by the firmware.
   * - `EFI_HII_CONFIG_ACCESS_PROTOCOL`
     - UEFI requires this for console devices, but it is rarely necessary in practice.
       Therefore this protocol is not required.
   * - `EFI_HII_CONFIG_ROUTING_PROTOCOL`
     - UEFI requires this for console devices, but it is rarely necessary in practice.
       Therefore this protocol is not required.
   * - Graphical console
     - Platforms with a graphical device are not required to expose it as a graphical console.
   * - `EFI_DISK_IO_PROTOCOL`
     - Rarely used interface that isn't required for EBBR use cases.
   * - `EFI_PXE_BASE_CODE_PROTOCOL`
     - Booting via the Preboot Execution Environment (PXE) is insecure.
       Loading via PXE is typically executed before launching the first UEFI application.
   * - Network protocols
     - A full implementation of the UEFI general purpose networking ABIs is not required,
       including `EFI_NETWORK_INTERFACE_IDENTIFIER_PROTOCOL`, `EFI_MANAGED_NETWORK_PROTOCOL`,
       `EFI_*_SERVICE_BINDING_PROTOCOL`, or any of the IPv4 or IPv6 protocols.
   * - Byte stream device support (UART)
     - UEFI protocols not required.
   * - PCI bus support
     - UEFI protocols not required.
   * - USB bus support
     - UEFI protocols not required.
   * - NVMe pass through support
     - UEFI protocols not required.
   * - SCSI pass through support
     - UEFI protocols not required.
   * - `EFI_DRIVER_FAMILY_OVERRIDE_PROTOCOL`
     - Not required.
   * - Option ROM support
     - In many EBBR use cases there is no requirement to generically support
       any PCIe add in card at the firmware level.
       When PCIe devices are used, drivers for the device are often built into
       the firmware itself rather than loaded as option ROMs.
       For this reason EBBR implementations are not required to support option
       ROM loading.

Required Global Variables
-------------------------

EBBR compliant platforms are required to support the following Global
Variables as found in :UEFI:`3.3`.

.. list-table:: Required UEFI Variables
   :widths: 50 50
   :header-rows: 1

   * - Variable Name
     - Description
   * - `Boot####`
     - A boot load option. `####` is a numerical hex value.
   * - `BootCurrent`
     - The boot option that was selected for the current boot.
   * - `BootNext`
     - The boot option that will be used for the next boot only.
   * - `BootOrder`
     - An ordered list of boot options.
       Firmware will try `BootNext` and each `Boot####` entry in the
       order given by `BootOrder` to find the first bootable image.
   * - `OsIndications`
     - Method for OS to request features from firmware.
   * - `OsIndicationsSupported`
     - Variable for firmware to indicate which features can be enabled.

.. _section-required-vars-for-on-disk:

Required Variables for capsule update "on disk"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the firmware implements in-band firmware update with `UpdateCapsule()` it
must support the following Variables to report the status of capsule "on disk"
processing after restart as found in :UEFI:`8.5.6`. [#FWUpNote]_

.. list-table:: UEFI Variables required for capsule update "on disk"
   :widths: 50 50
   :header-rows: 1

   * - Variable Name
     - Description
   * - `CapsuleNNNN`
     - Variable for firmware to report capsule processing status after restart.
       `NNNN` is a numerical hex value.
   * - `CapsuleMax`
     - Variable for platform to publish the maximum `CapsuleNNNN` supported.
   * - `CapsuleLast`
     - Variable for platform to publish the last `CapsuleNNNN` created.

.. [#FWUpNote] See section :ref:`section-fw-update`.

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
legitimately be loaded into either EL1 or EL2 on AArch64 and HS/VS/S mode on RISC-V.

AArch64 Exception Levels
------------------------

On AArch64 UEFI shall execute as 64-bit code at either EL1 or EL2, as defined in
:UEFI:`2.3.6`, depending on whether or not virtualization is available at OS
load time.

UEFI Boot at EL2
^^^^^^^^^^^^^^^^

Most systems are expected to boot UEFI at EL2, to allow for the installation of
a hypervisor or a virtualization aware Operating System.

UEFI Boot at EL1
^^^^^^^^^^^^^^^^

Booting of UEFI at EL1 is most likely employed within a hypervisor hosted Guest
Operating System environment, to allow the subsequent booting of a
UEFI-compliant Operating System.
In this instance, the UEFI boot-time environment can be provided, as a
virtualized service, by the hypervisor and not as part of the host firmware.

RISC-V Privilege Levels
-----------------------

RISC-V doesn't define dedicated privilege levels for hypervisor enabled platforms.
The supervisor mode becomes HS mode where a hypervisor or a hosting-capable
operating system runs while the guest OS runs in virtual S mode (VS mode).
Resident UEFI firmware can be executed in M mode or S/HS mode during POST.
However, the UEFI images must be loaded in HS or VS mode if virtualization
is available at OS load time.

UEFI Boot at S mode
^^^^^^^^^^^^^^^^^^^

Most systems are expected to boot UEFI at S mode when the hypervisor extension
is not enabled [RVPRIVSPEC]_.

UEFI Boot at HS mode
^^^^^^^^^^^^^^^^^^^^

Any platform supporting the hypervisor extension enabled most likely will boot UEFI at HS mode,
to allow for the installation of a hypervisor or a virtualization aware Operating System.

UEFI Boot at VS mode
^^^^^^^^^^^^^^^^^^^^

Booting of UEFI at VS mode is employed within a hypervisor hosted Guest Operating System environment,
to allow the subsequent booting of a UEFI-compliant Operating System.
In this instance, the UEFI boot-time environment can be provided,
as a virtualized service, by the hypervisor and not as part of the host firmware.

UEFI Configuration Tables
=========================

A UEFI system that complies with this specification may provide additional
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

EFI Conformance Profile Table
-----------------------------

The following GUID in the EFI Conformance Profile Table, as defined in
:UEFI:`4.6.5`, is used to indicate compliance to version 2.1.x of the EBBR
specification:

.. code-block:: c

    #define EFI_CONFORMANCE_PROFILE_EBBR_2_1_GUID \
    { 0xcce33c35, 0x74ac, 0x4087, \
    { 0xbc, 0xe7, 0x8b, 0x29, 0xb0, 0x2e, 0xeb, 0x27 }}

If the platform advertises an EBBR profile in the EFI Conformance Profile Table,
then it must be compliant with the corresponding version(s) of this
specification [#VersionsNote]_.

.. [#VersionsNote] This specification follows semantic versioning. As such,
   versions of this specification differing only by their last digit (or "patch
   number") are expected to be compatible.

Devicetree
----------

If firmware provides a Devicetree system description then it must be provided
in Flattened Devicetree Blob (DTB) format version 17 or higher as described in
[DTSPEC]_ § 5.
The DTB Nodes and Properties must be compliant with the requirements listed in
[DTSPEC]_ § 3 & 4 and with the requirements listed in the following table, which
take precedence.

.. list-table:: DTB Nodes and Properties requirements
   :widths: 50 50
   :header-rows: 1

   * - Name
     - Requirement
   * - ``/chosen``
     - This Node is required. ([DTSPEC]_ § 3.6)
   * - ``/chosen/stdout-path``
     - This Property is required. It is necessary for console output.
       ([DTSPEC]_ § 3.6)
   * - ``/chosen/efivarfile``
     - This Property is required when the EFI Variables are stored in a file as
       detailed in section :ref:`section-efi-vars-file-format`.

The DTB must be contained in memory of type `EfiACPIReclaimMemory`.
`EfiACPIReclaimMemory` was chosen to match the recommendation for ACPI
tables which fulfill the same task as the DTB.

UEFI Boot Services
==================

Memory Map
----------

The UEFI environment must provide a system memory map, which must include all
appropriate devices and memories that are required for booting and system
configuration.

All RAM defined by the UEFI memory map must be identity-mapped, which means
that virtual addresses must equal physical addresses.

The default RAM allocated attribute must be `EFI_MEMORY_WB`.

.. _section-misc-boot-services:

Miscellaneous Boot Services
---------------------------

The platform's monotonic counter is made optional.
If the platform does not implement the monotonic counter, the
`GetNextMonotonicCount()` function shall return `EFI_DEVICE_ERROR`. [#MonoNote]_

.. [#MonoNote] `EFI_UNSUPPORTED` is not an allowed status code for
   `GetNextMonotonicCount()`.

UEFI Secure Boot (Optional)
---------------------------

UEFI Secure Boot is optional for this specification.

If Secure Boot is implemented, it must conform to the UEFI specification for Secure Boot. There are no additional
requirements for Secure Boot.

UEFI Runtime Services
=====================

UEFI runtime services exist after the call to `ExitBootServices()` and are
designed to provide a limited set of persistent services to the platform
Operating System or hypervisor.
Functions contained in `EFI_RUNTIME_SERVICES` are expected to be available
during both boot services and runtime services.
However, it isn't always practical for all `EFI_RUNTIME_SERVICES` functions
to be callable during runtime services due to hardware limitations.
If any `EFI_RUNTIME_SERVICES` functions are only available during boot services
then firmware shall provide the `EFI_RT_PROPERTIES_TABLE` to
indicate which functions are available during runtime services.
Functions that are not available during runtime services shall return
`EFI_UNSUPPORTED`.

:numref:`uefi_runtime_service_requirements` details which `EFI_RUNTIME_SERVICES`
are required to be implemented during boot services and runtime services.

.. _uefi_runtime_service_requirements:
.. list-table:: `EFI_RUNTIME_SERVICES` Implementation Requirements
   :widths: 40 30 30
   :header-rows: 1

   * - `EFI_RUNTIME_SERVICES` function
     - Before `ExitBootServices()`
     - After `ExitBootServices()`
   * - `GetTime`
     - Required if RTC present.
     - Optional
   * - `SetTime`
     - Required if RTC present.
     - Optional
   * - `GetWakeupTime`
     - Required if wakeup supported.
     - Optional
   * - `SetWakeupTime`
     - Required if wakeup supported.
     - Optional
   * - `SetVirtualAddressMap`
     - N/A
     - Required
   * - `ConvertPointer`
     - N/A
     - Required
   * - `GetVariable`
     - Required
     - Optional
   * - `GetNextVariableName`
     - Required
     - Optional
   * - `SetVariable`
     - Required
     - Optional
   * - `GetNextHighMonotonicCount`
     - N/A
     - Optional
   * - `ResetSystem`
     - Required
     - Optional
   * - `UpdateCapsule`
     - Required for in-band update.
     - Optional
   * - `QueryCapsuleCapabilities`
     - Optional
     - Optional
   * - `QueryVariableInfo`
     - Optional
     - Optional

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

If an RTC is present, then `GetTime()` and `SetTime()` must be supported
before `ExitBootServices()` is called.

However, if firmware does not support access to the RTC after
`ExitBootServices()`, then `GetTime()` and `SetTime()` shall return `EFI_UNSUPPORTED`
and the OS must use a device driver to control the RTC.

UEFI Reset and Shutdown
-----------------------

`ResetSystem()` is required to be implemented in boot services, but it is
optional for runtime services.
During runtime services, the operating system should first attempt to
use `ResetSystem()` to reset the system.

If firmware doesn't support `ResetSystem()` during runtime services, then the call
will immediately return, and the OS should fall back to an architecture or
platform specific reset mechanism.

On AArch64 platforms implementing [PSCI]_,
if `ResetSystem()` is not implemented then the Operating System should fall
back to making a PSCI call to reset or shutdown the system.

Runtime Variable Access
-----------------------

There are many platforms where it is difficult to implement `SetVariable()` for
non-volatile variables during runtime services because the firmware cannot
access storage after `ExitBootServices()` is called.

e.g., If firmware accesses an eMMC device directly at runtime, it will
collide with transactions initiated by the OS.
Neither U-Boot nor Tianocore have a generic solution for accessing or updating
variables stored on shared media. [#OPTEESupplicant]_

If a platform does not implement modifying non-volatile variables with
`SetVariable()` after `ExitBootServices()`,
then firmware shall return `EFI_UNSUPPORTED` for any call to `SetVariable()`,
and must advertise that `SetVariable()` isn't available during runtime services
via the `RuntimeServicesSupported` value in the `EFI_RT_PROPERTIES_TABLE`
as defined in :UEFI:`4.6.2`.
EFI applications can read `RuntimeServicesSupported` to determine if calls
to `SetVariable()` need to be performed before calling `ExitBootServices()`.

Even when `SetVariable()` is not supported during runtime services, firmware
should cache variable names and values in `EfiRuntimeServicesData` memory so
that `GetVariable()` and `GetNextVariableName()` can behave as specified.

.. [#OPTEESupplicant] It is worth noting that OP-TEE has a similar problem
   regarding secure storage.
   OP-TEE's chosen solution is to rely on an OS supplicant agent to perform
   storage operations on behalf of OP-TEE.
   The same solution may be applicable to solving the UEFI non-volatile
   variable problem, but it requires additional OS support to work.
   Regardless, EBBR compliance does not require `SetVariable()` support
   during runtime services.

   https://optee.readthedocs.io/en/latest/architecture/secure_storage.html

.. _section-fw-update:

Firmware Update
---------------

Being able to update firmware to address security issues is a key feature of secure platforms.
EBBR platforms are required to implement either an in-band or an out-of-band firmware update mechanism.

If firmware update is performed in-band (firmware on the application processor updates itself),
then the firmware shall implement the `UpdateCapsule()` runtime service and accept updates in the
"Firmware Management Protocol Data Capsule Structure" format as described in
:UEFI:`23.3`. [#FMPNote]_
Firmware is also required to provide an EFI System Resource Table (ESRT) as
described in :UEFI:`23.4`.
Every firmware image that can be updated in-band must be described in the ESRT.
Firmware must support the delivery of capsules via file on mass storage device
("on disk") as described in :UEFI:`8.5.5`. [#VarNote]_

.. note::
   It is recommended that firmware implementing the `UpdateCapsule()` runtime
   service and an ESRT also implement the `EFI_FIRMWARE_MANAGEMENT_PROTOCOL`
   described in :UEFI:`23.1`. [#FMProtoNote]_

If firmware update is performed out-of-band (e.g., by an independent Baseboard
Management Controller (BMC), or firmware is provided by a hypervisor),
then the platform is not required to implement the `UpdateCapsule()` runtime
service and it is not required to provide an ESRT.

`UpdateCapsule()` is only required before `ExitBootServices()` is called.

.. [#FMPNote] The `UpdateCapsule()` runtime service is expected to be suitable
   for use by generic firmware update services like fwupd and Windows Update.
   Both fwupd and Windows Update read the ESRT table to determine what firmware
   can be updated, and use an EFI helper application to call `UpdateCapsule()`
   before `ExitBootServices()` is called.

   https://fwupd.org/

.. [#VarNote] Some Variables are required to support capsule "on disk".
   See section :ref:`section-required-vars-for-on-disk`.

.. [#FMProtoNote] At the time of writing, both Tianocore/EDK2 and U-Boot are
   using the `EFI_FIRMWARE_MANAGEMENT_PROTOCOL` internally to support their
   implementation of the `UpdateCapsule()` runtime service and of the ESRT,
   as detailed in :UEFI:`23.3` and :UEFI:`23.4` respectively.

Miscellaneous Runtime Services
------------------------------

If the platform does not implement the monotonic counter, it shall not support
the `GetNextHighMonotonicCount()` runtime service. [#BootNote]_

.. [#BootNote] The platform's monotonic counter is made optional in section
   :ref:`section-misc-boot-services`.
