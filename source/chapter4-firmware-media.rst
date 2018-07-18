.. SPDX-License-Identifier: CC-BY-SA-4.0

****************
Firmware Storage
****************

In general, EBBR compliant platforms should use dedicated storage for boot
firmware images and data,
independent of the storage used for OS partitions and the EFI System Partition
(ESP).
This could be a physically separate device (e.g. SPI flash),
or a dedicated logical unit (LU) within a device
(e.g. eMMC boot partition, [#eMMCBootPartition]_
or UFS boot LU [#LogicalUnitNote]_).

However, many embedded systems have size, cost, or implementation
constraints that make separate firmware storage unfeasible.
On such systems, firmware and the OS reside in the same storage device.
Care must be taken to ensure firmware kept in normal storage does not
conflict with normal usage of the media by an OS.

* Firmware must be stored on the media in a way that does not conflict
  with normal partitioning and usage by the operating system.
* Normal operation of the OS must not interfere with firmware files.
* Changing the partition table to switch from one OS to another must not
  interfere with firmware files.

  * In cases where the partition table has to be replaced instead of
    edited, it will not be possible to protect firmware during automated
    testing when switching between different operating systems.

* Firmware needs a method to modify variable storage at runtime while the
  OS controls access to the device. [#LUVariables]_

.. [#eMMCBootPartition] Watch out for the ambiguity of the word 'partition'.
   In most of this document, a 'partition' is a contiguous region of a block
   device as described by a GPT or MBR partition table,
   but eMMC devices also provide a dedicated 'boot partition' that is addressed
   separately from the main storage region, and does not appear in the
   partition table.

.. [#LogicalUnitNote] For the purposes of this document, logical units are
   treated as independent storage devices, each with their own GPT or MBR
   partition table.
   A platform that uses one LU for firmware, and another LU for OS partitions
   and the ESP is considered to be using dedicated firmware storage.

.. [#LUVariables] Runtime access to firmware data may still be an issue when
   firmware is stored in a dedicated LU, simply because the OS remains in
   control of the storage device command stream. If firmware doesn't have
   a dedicated channel to the storage device, then the OS must proxy all
   runtime storage IO.

Partitioning of Shared Storage
==============================

A shared storage device shall use GPT partitioning unless it is incompatible
with the platform boot sequence.
In which case, MBR partitioning shall be used. [#MBRReqExample]_

.. [#MBRReqExample] For example, if the boot ROM doesn't understand GPT
   partitioning, and will only work with an MBR, then the storage must be
   partitioned using an MBR.

.. warning::

   MBR partitioning is deprecated and only included for legacy support.
   All new platforms are expected to use GPT partitioning.
   GPT partitioning supports a much larger number of partitions, and
   has built in resiliency.

   A future issue of this specification will remove the MBR allowance.

Firmware images and data in shared storage should be contained
in partitions described by the GPT or MBR.
The platform should locate firmware by searching the partition table for
the partition(s) containing firmware.

However, some SoCs load firmware from a fixed offset into the storage media.
In this case, to protect against partitioning tools overwriting firmware, the
firmware image shall either reside entirely within the first 1MiB of storage,
or should be covered by a protective partition entry in the partition table as
described in sections :ref:`section-gpt-parts` and :ref:`section-mbr-parts`.

Automatic partitioning tools (e.g. an OS installer) must not create
partitions within the first 1MiB of storage, or delete, move, or modify
protective partition entries.
Manual partitioning tools should provide warnings when modifying
protective partitions or creating partitions within the first 1MiB.

.. warning::

   Fixed offsets to firmware data is supported only for legacy reasons.
   All new platforms are expected to use partitions to locate firmware files.

   A future issues of this specification will disallow the use of fixed
   offsets.

.. _section-gpt-parts:

GPT partitioning
----------------

The partition table must strictly conform to the UEFI specification and include
a protective MBR authored exactly as described in [UEFI]_ § 5 (hybrid
partitioning schemes are not permitted).

Protective partitions must have the Platform Required Attribute Flag set.

.. _section-mbr-parts:

MBR partitioning
^^^^^^^^^^^^^^^^

Protective partitions should have a partition type of 0xF8 unless some
immutable feature of the platform makes this impossible.

.. _section-fw-partition-fs:

Firmware Partition Filesystem
=============================

Where possible, firmware images and data should be stored in a filesystem.
Firmware can be stored either in a dedicated firmware partition,
or in certain circumstances in the UEFI System Partition (ESP).
Using a filesystem makes it simpler to manage multiple firmware files and
makes it possible for a single disk image to contain firmware for multiple
platforms.

When firmware is stored in the ESP, the ESP should contain a partition named
``/FIRMWARE`` in the root directory,
and all firmware images and data should be stored in platform vendor
subdirectories under ``/FIRMWARE``.

Dedicated firmware partitions should be formatted with a FAT
filesystem as defined by the UEFI specification.
Dedicated firmware partitions should use the same ``/FIRMWARE`` directory
hierarchy.
OS tools shall ignore dedicated firmware partitions,
and shall not attempt to use a dedicated firmware partition as an ESP.

Vendors may choose their own subdirectory name under ``/FIRMWARE``,
but shall choose names the do not conflict with other vendors.
Normally the vendor name will be the name of the SoC vendor, because the
firmware directory name will be hard coded in the SoC's boot ROM.
Vendors are recommended to use their Devicetree vendor prefix as their
vendor subdirectory name.

Vendors are free to decide how to structure subdirectories under their
own vendor directory, but they shall use a naming convention that allows
multiple SoCs to be supported in the same filesystem.

For example, a vendor named Acme with two SoCs, AM100 & AM300, could
choose to use the SoC part number as a subdirectory in the firmware path::

  /FIRMWARE
    /ACME
      /AM100
        fw.img
      /AM300
        fw.img

It is also recommended for dedicated firmware partitions to use the
``/FIRMWARE`` file hierarchy.

The following is a sample directory structure for firmware files::

  /FIRMWARE
    /<Vendor 1 Directory>
       /<SoC A Directory>
          <Firmware image>
          <Firmware data>
       /<SoC B Directory>
          <Firmware image>
          <Firmware data>
    /<Vendor 2 Directory>
       <Common Firmware image>
       <Common Firmware data>
    /<Vendor 3 Directory>
       /<SoC E Directory>
          <Firmware image>

Operating systems and installers should not manipulate any files in the
``/FIRMWARE`` hierarchy during normal operation.

.. todo:

   * Recommend failover A/B image layout to protect against corrupted
     firmware.
   * Define firmware update procedure. In what circumstances could an
     OS automatically update firmware files in ``/FIRMWARE``?

The sections below discuss the requirements when using both fixed and
removable storage.
However, it should be noted that the recommended behaviour of firmware
should be identical regardless of storage type.
In both cases, the recommended boot sequence is to first search for firmware
in a dedicated firmware partition, and second search for firmware in the
ESP.
The only difference between fixed and removable storage is the recommended
factory settings for the platform.


Fixed Shared Storage
--------------------

Fixed storage is storage that is permanently attached to the platform,
and cannot be moved between systems.
eMMC and Universal Flash Storage (UFS) device are often used as
shared fixed storage for both firmware and the OS.

Where possible, it is prefered for the system to boot from a dedicated boot
region on media that provides one (e.g., eMMC) that is sufficiently large.
Otherwise, the platform storage should be pre-formatted in the factory with
a partition table, a dedicated firmware partition, and firmware binaries
installed.

Operating systems must not use the dedicated firmware partition for installing
EFI applications including, but not limited to, the OS loader and OS specific
files. Instead, a normal ESP should be created.
OS partitioning tools must take care not to modify or delete dedicated
firmware partitions.

Removable Shared Storage
------------------------

Removable storage is any media that can be physically removed from
the system and moved to another machine as part of normal operation
(e.g., SD cards, USB thumb drives, and CDs).

There are two primary scenarios for storing firmware on removable media.

1. Platforms that only have removable media (e.g., The Raspberry Pi has an
   SD card slot, but no fixed storage).
2. Recovery when on-board firmware has been corrupted. If firmware on
   fixed media has been corrupted, some platforms support loading firmware
   from removable media which can then be used to recover the platform.

In both cases, it is desirable to start with a stock OS boot image,
copy it to the media (SD or USB), and then add the necessary firmware files
to make the platform bootable.
Typically, OS boot images won't include a dedicated firmware partition,
and it is inconvenient to repartition the media to add one.
It is simpler and easier for the user if they are able to copy
the required firmware files into the ``/FIRMWARE`` directory tree on the ESP
using the basic file manager tools provided by all desktop operating systems.

On removable media, firmware should be stored in the ESP under the
``/FIRMWARE`` directory structure as described in
:ref:`section-fw-partition-fs`.
Platform vendors should support their platform by providing a single
.zip file that places all the required firmware files in the correct
locations when extracted in the ESP ``/FIRMWARE`` directory.
For simplicity sake, it is expected the same .zip file will recover the
firmware files in a dedicated firmware partition.
