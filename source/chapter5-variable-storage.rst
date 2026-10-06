.. SPDX-License-Identifier: CC-BY-SA-4.0

********************
EFI Variable Storage
********************

.. versionadded:: 2.2.0

Some UEFI enabled devices can only store EFI variables as a file on a block
device. This implies that at runtime the operating system must manage changes
to the EFI variables by updating the file.

This chapter defines a file format for EFI variables that both the firmware
and the operating system can rely on, and describes, as an example, a
mechanism that keeps the variable runtime services available with such a
file-backed variable store, as implemented by U-Boot and the libefivar
library.

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

Runtime Access to File-Backed Variables (non-normative)
=======================================================

This section is non-normative. It describes, as an example, a mechanism that
keeps the variable runtime services available with a file-backed variable
store: the firmware services the variable runtime services from a copy of the
variable store held in memory, and the operating system writes the modified
variable store back to the EFI System Partition. U-Boot, which implements the
firmware side of the mechanism since release v2024.07, and the libefivar
library, which implements the operating system side, are used as example
implementations throughout this section. Other firmware implements the same
mechanism, e.g., the EDK II based firmware of Qualcomm platforms. This
specification requires neither firmware nor operating systems to implement
this mechanism, including the variables described below. See section
:ref:`section-runtime-variable-access` for the requirements on the variable
runtime services.

Firmware that stores EFI variables in a file usually cannot write to that
file after `ExitBootServices()`: the file resides on a storage device that is
controlled by the operating system at runtime, and any firmware access would
conflict with transactions initiated by the OS.

The firmware keeps a copy of the variable store in `EfiRuntimeServicesData`
memory, services `GetVariable()`, `GetNextVariableName()` and `SetVariable()`
from that copy during runtime services, and advertises `SetVariable()` as
supported in the `EFI_RT_PROPERTIES_TABLE`. Calls to `SetVariable()` during
runtime services only modify the in-memory copy, without accessing the
variable store file. The modifications are therefore volatile, including
those to variables carrying the `EFI_VARIABLE_NON_VOLATILE` attribute, until
the operating system writes the variable store back to the file as described
below. U-Boot implements this when built with the `EFI_RT_VOLATILE_STORE`
configuration option.

Which modifications are accepted during runtime services is up to the
implementation. U-Boot only accepts modifications of non-volatile variables
having the `EFI_VARIABLE_RUNTIME_ACCESS` attribute: authenticated variables
are not supported, volatile variables cannot be created or modified,
variables without the `EFI_VARIABLE_RUNTIME_ACCESS` attribute are hidden from
`GetVariable()` and `GetNextVariableName()` and cannot be created or
modified, and the attributes of an existing variable cannot be changed.

Variables
---------

The firmware exposes the variable store file to the operating system through
the two variables described below, under the vendor GUID
`b2ac5fc9-92b7-4acd-aeac-11e818c3130c`, which U-Boot defines as
`U_BOOT_EFI_RT_VAR_FILE_GUID`:

.. code-block:: c

    #define U_BOOT_EFI_RT_VAR_FILE_GUID \
        EFI_GUID(0xb2ac5fc9, 0x92b7, 0x4acd, \
                 0xae, 0xac, 0x11, 0xe8, 0x18, 0xc3, 0x13, 0x0c)

Both variables have the `EFI_VARIABLE_BOOTSERVICE_ACCESS` and
`EFI_VARIABLE_RUNTIME_ACCESS` attributes, are volatile, and are read-only:
calls to `SetVariable()` targeting them fail with `EFI_WRITE_PROTECTED`.

RTStorageVolatile
    This variable contains the path of the variable store file, relative to
    the root directory of the EFI System Partition, as a NUL terminated ASCII
    string. Any file path on the EFI System Partition can be used:
    `ubootefi.var`, in the root directory, is the file name U-Boot uses.

VarToFile
    This variable contains the complete content the variable store file needs
    to hold in order to persist the current state of all variables carrying
    the `EFI_VARIABLE_NON_VOLATILE` attribute, as an `EFI_VARIABLE_FILE`
    image in the format defined in this chapter. The firmware regenerates
    the content every time the variable is read, so that it reflects all
    preceding `SetVariable()` calls, including calls made during runtime
    services.

Persisting variable modifications
---------------------------------

To persist a variable modification performed during runtime services, the
operating system reads `RTStorageVolatile` to obtain the path of the variable
store file, reads `VarToFile` after the modification, and writes its content
to the variable store file on the EFI System Partition.

The libefivar library, which Linux tools such as efibootmgr use to access EFI
variables, implements the operating system side: it detects the mechanism by
looking up `RTStorageVolatile` under the GUID above, and performs this
write-back after each variable modification or deletion it carries out, so
that the tools built on it persist their modifications transparently.
[#LibefivarNote]_ It only updates an existing variable store file, which it
locates by probing the usual mount points of the EFI System Partition.

.. [#LibefivarNote] libefivar commit 68daa046 ("efivarfs: Update a file
   variable store On SetVariable RT"),
   https://github.com/rhboot/efivar/commit/68daa04654acbe1bbaa17ebfc23c371b39e69c6b

   At the time of writing, this support is not yet part of a tagged release
   of libefivar.

Writing the new content to a temporary file on the same partition, flushing
it to the storage device, then renaming it over the variable store file,
limits the exposure to an interrupted update: the content is complete before
the rename, which the file system performs as a single operation, and an
update interrupted before the rename leaves the variable store file
untouched. On Linux, `rename()` provides this on FAT file systems like on
any other file system, and since Linux 6.0 the FAT driver also supports the
`RENAME_EXCHANGE` flag of `renameat2()`, which exchanges the temporary file
and the variable store file in a single operation, as transactional as a
file system without a journal allows. [#RenameExchangeNote]_

.. [#RenameExchangeNote] Linux commit da87e1725ae2 ("fat: add renameat2
   RENAME_EXCHANGE flag support"),
   https://git.kernel.org/linus/da87e1725ae2136baeb9aac04c572c283afc917f

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

The mechanism described in section :ref:`section-runtime-var-handover` does
not provide generic `SetVariable()` support during runtime services: only the
modifications performed through software implementing the operating system
side of the mechanism are persisted, which at the time of writing means only
the modifications performed by tools using libefivar, such as efibootmgr.
Modifications performed by other means, e.g., by an application writing
directly to the `efivarfs` file system of the Linux kernel, or by an
operating system without support for the mechanism, are lost when the system
resets. Additionally, on systems with multiple EFI System Partitions,
`RTStorageVolatile` names the variable store file but not the partition
holding it, so identifying the correct partition is left to the operating
system.
