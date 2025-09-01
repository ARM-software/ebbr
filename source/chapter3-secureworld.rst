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

Platforms without EL3 must implement PSCI and SMCCC at EL2 (leaving only EL1
available to an operating system).

It is recommended that firmware implements PSCI version 1.0 or later
[#PSCINote]_ and SMCCC version 1.1 or later [#SMCCCNote]_.

.. [#PSCINote] PSCI version 1.0 is considered as an errata fix release for
   version 0.2, where functions interfaces have been stabilized.
   It also introduced the `PSCI_FEATURES` function, for standardized discovery.

.. [#SMCCCNote] Starting with SMCCC version 1.1, support for the `SMCCC_VERSION`
   function is required, for standardized discovery.

.. warning:: A future version of this specification will require minimum PSCI
   and SMCCC versions.

AArch64 Firmware Framework
==========================

On AArch64 platforms, when privileged or secure firmware implements the Firmware
Framework for A-profile (FF-A), it must conform to the Arm Firmware Framework
for Arm A-profile specification [FFA]_ and it must support at least one callee
version compatible with caller version 1.2. [#FFANote]_

.. [#FFANote] FF-A is an Arm software architecture describing interfaces that
   standardize communication between software images and firmware, in the Secure
   world and the Normal world.
   FF-A v1.2 introduced support for multiple services UUIDs in a partition,
   which eases services discovery, as well as the supporting
   `FFA_MSG_SEND_DIRECT_REQ2` ABI.
   As per the FF-A specification [FFA]_ § 13.2 FFA_VERSION, all callee versions
   1.x, with x >= 2, are compatible with caller versions 1.0 to 1.x, which
   includes caller version 1.2.

AArch64 System Control and Management
=====================================

On AArch64 platforms, when privileged or secure firmware implements the System
Control and Management Interface (SCMI), it must conform to the Arm System
Control and Management Interface specification [SCMI]_ and it must implement a
Base protocol version 2.x, where x >= 1 is recommended. [#SCMINote]_

.. [#SCMINote] SCMI is a set of software interfaces defined by Arm, used in
   the system management of power domains, performances, clocks, sensors, reset,
   voltage domains, power and pins.
   SCMI specification v3.2 introduced Base Protocol v2.1 and the
   `NEGOTIATE_PROTOCOL_VERSION` command, which eases agents and platforms
   interoperability.
   Future versions 3.x are not guaranteed to retain compatibility with current
   agents, which forbids their use to start exchanging messages.
   This should not prevent agents and platforms to exchange messages with future
   versions 3.x, after negotiation.

.. warning:: A future version of this specification will require a minimum SCMI
   Base protocol version of 2.1.

RISC-V Multiprocessor Startup Protocol
======================================

The resident firmware in M mode or hypervisor running in HS mode must implement
and conform to at least SBI [RVSBISPEC]_ v0.2 with HART State Management(HSM)
extension for both RV32 and RV64.
