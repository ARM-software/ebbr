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
At `ExitBootServices()` time, all secondary CPUs must be parked or powered off.

AArch64 Multiprocessor Startup Protocol
=======================================
On AArch64 platforms, Firmware resident in Trustzone EL3 must implement and
conform to the Power State Coordination Interface specification [PSCI]_ and to
the SMC Calling Convention [SMCCC]_.

Platforms without EL3 must implement one of:

- PSCI and SMCCC at EL2 (leaving only EL1 available to an operating system)
- Linux AArch64 spin tables [LINUXA64BOOT]_ (Devicetree only)

However, the spin table protocol is strongly discouraged.
Future versions of this specification will only allow PSCI and SMCCC, and they
should be implemented in all new designs.

It is recommended that firmware implementing PSCI supports version 1.0 or later
[#PSCINote]_ and that firmware implementing SMCCC supports version 1.1 or later
[#SMCCCNote]_.

.. [#PSCINote] PSCI version 1.0 is considered as an errata fix release for
   version 0.2, where functions interfaces have been stabilized.
   It also introduced the `PSCI_FEATURES` function, for standardized discovery.

.. [#SMCCCNote] Starting with SMCCC version 1.1, support for the `SMCCC_VERSION`
   function is required, for standardized discovery.

RISC-V Multiprocessor Startup Protocol
======================================
The resident firmware in M mode or hypervisor running in HS mode must implement
and conform to at least SBI [RVSBISPEC]_ v0.2 with HART State Management(HSM)
extension for both RV32 and RV64.
