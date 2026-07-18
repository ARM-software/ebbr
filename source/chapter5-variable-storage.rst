.. SPDX-License-Identifier: CC-BY-SA-4.0

********************
EFI Variable Storage
********************

.. versionadded:: 2.2.0

Some UEFI enabled devices can only store EFI variables as a file on a block
device. This implies that at runtime the operating system must manage changes
to the EFI variables by updating the file.

This chapter defines a file format for EFI variables that both the firmware
and the operating system can rely on, as well as a mechanism allowing the
operating system to persist variable modifications made with `SetVariable()`
during runtime services on behalf of the firmware.

File Format For Storing EFI Variables
=====================================

All integer fields are stored in little-endian byte order.

File header
-----------

The following byte sequence is used to identify the file format:

.. code-block:: c

    #define EFI_VAR_FILE_MAGIC {0x55, 0x62, 0x45, 0x66, 0x69, 0x56, 0x61}

The current revision of the file format is given by:

.. code-block:: c

    #define EFI_VAR_FILE_FORMAT_REVISION_1 1

The file header has the following structure:

.. code-block:: c

    typedef struct {
        UINT64                  Reserved;
        UINT8                   Magic[7];
        UINT8                   Revision;
        UINT32                  Length;
        UINT32                  Crc32;
        EFI_VARIABLE_ENTRY      Variables[];
    } EFI_VARIABLE_FILE;

Reserved
    This field is not used currently. Its value shall be set to 0.

Magic
    This field is used to identify the file as containing EFI variables.
    Its value is `EFI_VAR_FILE_MAGIC`.

Revision
    This field contains the revision of the file format. As of this revision it
    takes the value `EFI_VAR_FILE_FORMAT_REVISION_1`.

Length
    This field contains the length in bytes of the structure `EFI_VARIABLE_FILE`
    and all entries in `Variables` entries. The actual file may be longer.

Crc32
    This field contains the value of the CRC32 of all variable entries.
    The first byte to hash is given by the offset of field `Variables`. The
    number of bytes to hash is given by `Length` minus the size of
    `EFI_VARIABLE_FILE`.

Variables
    The list of variables entries starts at this field. Each variable entry is
    expanded with NUL bytes to a multiple of 8 bytes. The list of variables is
    not sorted.

Variable entries
----------------

Each variable is stored as a structure:

.. code-block:: c

    typedef struct {
        UINT32          DataSize;
        UINT32          Attributes;
        UINT64          TimeStamp;
        EFI_GUID        VendorGuid;
        UINT8           Data[];
    } EFI_VARIABLE_ENTRY;

DataSize
    This field contains the size of the `Data` field in bytes without
    the NUL terminated variable name.

Attributes
    This field is a bitmap with the variable attributes as defined in
    :UEFI:`8.2.1`.

TimeStamp
    For time-based authenticated variables this field contains the timestamp
    associated with the authentication descriptor encoded as seconds since
    1970-01-01T00:00:00Z. For all other variables this field shall be set to 0.

VendorGuid
    This field contains the unique identifier of the vendor.

Data
    This field contains a NUL terminated UCS-2 string with the name of the
    vendor’s variable followed by `DataSize` bytes of actual content of the
    variable.

.. _section-runtime-var-handover:

Runtime Access to File-Backed Variables
=======================================

.. versionadded:: 2.5.0

Firmware that stores EFI variables in a file usually cannot write to that
file after `ExitBootServices()`: the file resides on a storage device that is
controlled by the operating system at runtime, and any firmware access would
conflict with transactions initiated by the OS.

This section defines a mechanism through which such firmware keeps the
variable runtime services available after `ExitBootServices()` by servicing
them from memory, and delegates writing the variable store file to the
operating system. See section :ref:`section-runtime-variable-access` for when
implementing this mechanism is required.

Handover variables
------------------

Firmware implementing this mechanism shall provide the two variables
described below under the following vendor GUID: [#GuidNote]_

.. code-block:: c

    #define EBBR_RT_VAR_FILE_GUID \
    { 0xb2ac5fc9, 0x92b7, 0x4acd, \
    { 0xae, 0xac, 0x11, 0xe8, 0x18, 0xc3, 0x13, 0x0c }}

.. [#GuidNote] The GUID value is fixed by existing implementations of this
   mechanism. U-Boot defines it as `U_BOOT_EFI_RT_VAR_FILE_GUID`, and the
   libefivar library detects the mechanism by looking up `RTStorageVolatile`
   under this GUID.

Both variables shall have the `EFI_VARIABLE_BOOTSERVICE_ACCESS` and
`EFI_VARIABLE_RUNTIME_ACCESS` attributes, shall not have the
`EFI_VARIABLE_NON_VOLATILE` attribute, and shall be read-only: any call to
`SetVariable()` targeting them shall fail with `EFI_WRITE_PROTECTED`.

RTStorageVolatile
    This variable contains the name of the variable store file as a NUL
    terminated ASCII string. The file is located in the root directory of the
    EFI System Partition holding the variable store, and the value shall not
    contain any directory separator. E.g., U-Boot stores its EFI variables in
    the file `ubootefi.var`.

VarToFile
    This variable contains the complete content that the variable store file
    must have in order to persist the current state of all EFI variables
    carrying the `EFI_VARIABLE_NON_VOLATILE` attribute. Firmware shall
    regenerate the content every time the variable is read, so that it
    reflects all preceding `SetVariable()` calls, including calls made during
    runtime services.

    The operating system shall treat the content as an opaque binary blob.
    Firmware using the file format defined in this chapter returns an
    `EFI_VARIABLE_FILE` image holding all variables that have the
    `EFI_VARIABLE_NON_VOLATILE` attribute set. [#FormatNote]_

.. [#FormatNote] The mechanism does not depend on the store file format,
   as the operating system never interprets the store file content.
   Firmware is nevertheless encouraged to use the file format defined in
   this chapter.

Firmware requirements
---------------------

Firmware implementing this mechanism shall:

- Maintain a copy of the variable store in `EfiRuntimeServicesData` memory,
  and service `GetVariable()` and `GetNextVariableName()` from that copy
  during runtime services.

- Implement `SetVariable()` during runtime services by applying the
  modification to the in-memory store, without accessing the variable store
  file. Modifications are consequently volatile until the operating system
  writes them back to the store file, including modifications to variables
  that have the `EFI_VARIABLE_NON_VOLATILE` attribute.

- Advertise `EFI_RT_SUPPORTED_GET_VARIABLE`,
  `EFI_RT_SUPPORTED_GET_NEXT_VARIABLE_NAME` and
  `EFI_RT_SUPPORTED_SET_VARIABLE` in the `EFI_RT_PROPERTIES_TABLE` described
  in :UEFI:`4.6.2`.

The in-memory store imposes restrictions during runtime services. The
following operations shall fail:

- Creating, modifying, or deleting authenticated variables (see
  `Limitations`_ below).

- Creating, modifying, or deleting volatile variables.

- Modifying or deleting variables that do not have the
  `EFI_VARIABLE_RUNTIME_ACCESS` attribute. These variables shall also be
  hidden from `GetVariable()` and `GetNextVariableName()`.

- Changing the attributes of an existing variable.

Operating system requirements
-----------------------------

To make a variable modification performed during runtime services
persistent, the operating system shall:

1. Read the `RTStorageVolatile` variable to obtain the name of the variable
   store file, and locate that file in the root directory of the EFI System
   Partition.

2. Read the `VarToFile` variable after the modification.

3. Write the content of `VarToFile` to the variable store file.

Modifications that have not been written back to the variable store file,
including modifications to variables that have the
`EFI_VARIABLE_NON_VOLATILE` attribute, are lost when the system resets.

The operating system should update the variable store file atomically, so
that an interrupted update cannot corrupt the store. The variable store file
is created by the firmware; the operating system should only update an
existing file, and should not create the file when it is absent.

Limitations
===========

The security of a file based variable storage is limited by the security
of the storage or transport medium. Without further measures file storage
is inadequate for the UEFI security database and other authenticated
variables.

The current version of the file format can convey the timestamp of
time-based authenticated variables. It does not define the storage of the
signing certificates of nonce-based authenticated variables. [#CertNote]_

.. [#CertNote] Tianocore EDK II keeps signer certificates of authenticated
   variables in variables `certdb` and `certdbv`.

Variables modified through the mechanism described in
:ref:`section-runtime-var-handover` only persist across reset if the
operating system writes the updated store content back to the variable store
file. Additionally, on systems with multiple EFI System Partitions,
`RTStorageVolatile` names the variable store file but not the partition
holding it, so identifying the correct partition is left to the operating
system.
