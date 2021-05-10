.. SPDX-License-Identifier: CC-BY-SA-4.0

*****************************
Privileged or Secure Firmware
*****************************

AArch32 Multiprocessor Startup Protocol
=======================================
There is no standard multiprocessor startup or CPU power management mechanism
for ARMv7 and earlier platforms.
The OS is expected to use platform specific drivers for CPU power management.
Firmware must advertize the CPU power management mechanism in the Devicetree
system description or the ACPI tables so that the OS can enable the correct
driver.
At ExitBootServices() time, all secondary CPUs must be parked or powered off.

AArch64 Multiprocessor Startup Protocol
=======================================
On AArch64 platforms, Firmware resident in Trustzone EL3 must implement and
conform to the Power State Coordination Interface specification [PSCI]_.

Platforms without EL3 must implement one of:

- PSCI at EL2 (leaving only EL1 available to an operating system)
- Linux AArch64 spin tables [LINUXA64BOOT]_ (Devicetree only)

However, the spin table protocol is strongly discouraged.
Future versions of this specification will only allow PSCI, and PSCI should
be implemented in all new designs.

RISC-V Multiprocessor Startup Protocol
======================================
The resident firmware in M mode or hypervisor running in HS mode must implement
and conform to at least SBI [RVSBISPEC]_ v0.2 with HART State Management(HSM)
extension for both RV32 and RV64.
The firmware must also provide a devicetree containing a ``boot-hartid`` property
under the ``/chosen`` node before jumping to a UEFI application.
This property must indicate the id of the booting HART.
