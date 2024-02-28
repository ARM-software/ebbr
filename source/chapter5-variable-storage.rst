.. SPDX-License-Identifier: CC-BY-SA-4.0

.. _section-efi-vars-file-format:

*************************************
File Format For Storing EFI Variables
*************************************

Some UEFI enabled devices can only store EFI variables as a file on a block
device. This implies that at runtime the operating system must manage changes
to the EFI variable by updating the file.

This chapter defines a file-format for EFI variables that both the firmware
and the operating system can rely on.

All integer fields are stored in little-endian byte order.

File header
===========

The following byte sequence is used to identify the file format:

.. code-block:: c

    #define EFI_VAR_FILE_MAGIC {0x55, 0x62, 0x45, 0x66, 0x69, 0x56, 0x61}

The current revision of the file format it given by:

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
================

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
    This field is a bitmap with the variable attributes [#AttrNote]_.

TimeStamp
    For time-based authenticaed variables this field contains the timestamp
    associated with the authentication descriptor encoded as seconds since
    1970-01-01T00:00:00Z. For all other variables this field shall be set to 0.

VendorGuid
    This field contains the unique identifier of the vendor.

Data
    This field contains a NUL terminated UCS-2 string with the name of the
    vendor’s variable followed by `DataSize` bytes of actual content of the
    variable.

.. [#AttrNote] As defined in :UEFI:`8.2.1`.

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
