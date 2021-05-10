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

EBBR compliant platform shall conform to a subset of the [UEFI]_ spec as listed
in this section.
Normally, UEFI compliance would require full compliance with all items listed
in UEFI § 2.6.
However, the EBBR target market has a reduced set of requirements,
and so some UEFI features are omitted as unnecessary.

Required Elements
-----------------

This section replaces the list of required elements in [UEFI]_ § 2.6.1.
All of the following UEFI elements are required for EBBR compliance.

.. list-table:: UEFI Required Elements
   :widths: 50 50
   :header-rows: 1

   * - Element
     - Requirement
   * - `EFI_SYSTEM_TABLE`
     - The system table is required to provide required to access UEFI Boot Services,
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
     - Must be installed for each loaded image
   * - `EFI_LOADED_IMAGE_DEVICE_PATH_PROTOCOL`
     - Must be installed for each loaded image
   * - `EFI_DEVICE_PATH_PROTOCOL`
     - An `EFI_DEVICE_PATH_PROTOCOL` must be installed onto all device
       handles provided by the firmware.
   * - `EFI_DEVICE_PATH_UTILITIES_PROTOCOL`
     - Interface for creating and manipulating UEFI device paths

.. list-table:: Notable omissions from UEFI § 2.6.1
   :header-rows: 1

   * - Element
     - Note
   * - `EFI_DECOMPRESS_PROTOCOL`
     - Native EFI decompression is rarely used and therefore not required.

Required Platform Specific Elements
-----------------------------------

This section replaces the list of required elements in [UEFI]_ § 2.6.2.
All of the following UEFI elements are required for EBBR compliance.

.. list-table:: UEFI Platform-Specific Required Elements
   :widths: 50 50
   :header-rows: 1

   * - Element
     - Description
   * - Console devices
     - The platform must have at least one console device
   * - `EFI_SIMPLE_TEXT_INPUT_PROTOCOL`
     - Needed for console input
   * - `EFI_SIMPLE_TEXT_INPUT_EX_PROTOCOL`
     - Needed for console input
   * - `EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL`
     - Needed for console output
   * - `EFI_DEVICE_PATH_TO_TEXT_PROTOCOL`
     - Needed for console output
   * - `EFI_HII_STRING_PROTOCOL`
     - Required by EFI shell and for compliance testing
   * - `EFI_HII_DATABASE_PROTOCOL`
     - Required by EFI shell and for compliance testing
   * - `EFI_UNICODE_COLLATION2_PROTOCOL`
     - Required by EFI shell and for compliance testing
   * - `EFI_BLOCK_IO_PROTOCOL`
     - Required for block device access
   * - `EFI_SIMPLE_FILE_SYSTEM_PROTOCOL`
     - Required if booting from block device is supported
   * - `EFI_RNG_PROTOCOL`
     - Required if the platform has a hardware entropy source
   * - `EFI_SIMPLE_NETWORK_PROTOCOL`
     - Required if the platform has a network device.
   * - HTTP Boot (UEFI § 24.7)
     - Required if the platform supports network booting

The following table is a list of notable deviations from UEFI § 2.6.2.
Many of these deviations are because the EBBR use cases do not require
interface specific UEFI protocols, and so they have been made optional.

.. list-table:: Notable Deviations from UEFI § 2.6.2
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
     - Rarely used interface that isn't required for EBBR use cases
   * - `EFI_PXE_BASE_CODE_PROTOCOL`
     - Booting via the Preboot Execution Environment (PXE) is insecure.
       Loading via PXE is typically executed before launching the first UEFI application.
   * - Network protocols
     - A full implementation of the UEFI general purpose networking ABIs is not required,
       including `EFI_NETWORK_INTERFACE_IDENTIFIER_PROTOCOL`, `EFI_MANAGED_NETWORK_PROTOCOL`,
       `EFI_*_SERVICE_BINDING_PROTOCOL`, or any of the IPv4 or IPv6 protocols.
   * - Byte stream device support (UART)
     - UEFI protocols not required
   * - PCI bus support
     - UEFI protocols not required
   * - USB bus support
     - UEFI protocols not required
   * - NVMe pass through support
     - UEFI protocols not required
   * - SCSI pass through support
     - UEFI protocols not required
   * - `EFI_DRIVER_FAMILY_OVERRIDE_PROTOCOL`
     - Not required
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
Variables as found in [UEFI]_ § 3.3.

.. list-table:: Required UEFI Variables
   :widths: 25 75
   :header-rows: 1

   * - Variable Name
     - Description
   * - `Boot####`
     - A boot load option. `####` is a numerical hex value
   * - `BootCurrent`
     - The boot option that was selected for the current boot
   * - `BootNext`
     - The boot option that will be used for the next boot only
   * - `BootOrder`
     - An ordered list of boot options.
       Firmware will try `BootNext` and each `Boot####` entry in the
       order given by BootOrder to find the first bootable image.
   * - `OsIndications`
     - Method for OS to request features from firmware
   * - `OsIndicationsSupported`
     - Variable for firmware to indicate which features can be enabled

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

On AArch64 UEFI shall execute as 64-bit code at either EL1 or EL2,
depending on whether or not virtualization is available at OS load time.

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

Most systems are expected to boot UEFI at S mode as the hypervisor extension
[RVHYPSPEC]_ is still in draft state.

UEFI Boot at HS mode
^^^^^^^^^^^^^^^^^^^^

Any platform with hypervisor extension enabled most likely to boot UEFI at HS mode,
to allow for the installation of a hypervisor or a virtualization aware Operating System.

UEFI Boot at VS mode
^^^^^^^^^^^^^^^^^^^^

Booting of UEFI at VS mode is employed within a hypervisor hosted Guest Operating System environment,
to allow the subsequent booting of a UEFI-compliant Operating System.
In this instance, the UEFI boot-time environment can be provided,
as a virtualized service, by the hypervisor and not as part of the host firmware.

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

Configuration Tables
--------------------

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
     - Required if RTC present
     - Optional
   * - `SetTime`
     - Required if RTC present
     - Optional
   * - `GetWakeupTime`
     - Required if wakeup supported
     - Optional
   * - `SetWakeupTime`
     - Required if wakeup supported
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
   * - `GetNextVeriableName`
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
     - Required for in-band update
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
as defined in [UEFI]_ § 4.6.
EFI applications can read `RuntimeServicesSupported` to determine if calls
to `SetVariable()` need to be performed before calling `ExitBootServices()`.

Even when `SetVariable()` is not supported during runtime services, firmware
should cache variable names and values in EfiRuntimeServicesData memory so
that `GetVariable()` and `GetNextVeriableName()` can behave as specified.

Firmware Update
---------------

Being able to update firmware to address security issues is a key feature of secure platforms.
EBBR platforms are required to implement either an in-band or an out-of-band firmware update mechanism.

If firmware update is performed in-band (firmware on the application processor updates itself),
then the firmware shall implement the `UpdateCapsule()` runtime service and accept updates in the
"Firmware Management Protocol Data Capsule Structure" format as described in [UEFI]_ § 23.3,
"Delivering Capsules Containing Updates to Firmware Management Protocol.  [#FMPNote]_
Firmware is also required to provide an EFI System Resource Table (ESRT). [UEFI]_ § 23.4
Every firmware image that can be updated in-band must be described in the ESRT.

If firmware update is performed out-of-band (e.g., by an independent Baseboard
Management Controller (BMC), or firmware is provided by a hypervisor),
then the platform is not required to implement the `UpdateCapsule()` runtime service.

`UpdateCapsule()` is only required before `ExitBootServices()` is called.


.. [#OPTEESupplicant] It is worth noting that OP-TEE has a similar problem
   regarding secure storage.
   OP-TEE's chosen solution is to rely on an OS supplicant agent to perform
   storage operations on behalf of OP-TEE.
   The same solution may be applicable to solving the UEFI non-volatile
   variable problem, but it requires additional OS support to work.
   Regardless, EBBR compliance does not require `SetVariable()` support
   during runtime services.

   https://optee.readthedocs.io/en/latest/architecture/secure_storage.html

.. [#FMPNote] The `UpdateCapsule()` runtime service is expected to be suitable
   for use by generic firmware update services like fwupd and Windows Update.
   Both fwupd and Windows Update read the ESRT table to determine what firmware
   can be updated, and use an EFI helper application to call `UpdateCapsule()`
   before `ExitBootServices()` is called.

   https://fwupd.org/
