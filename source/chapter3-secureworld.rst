******************************
Priviledged or Secure Firmware
******************************

Multiprocessor Startup Protocol
===============================
Firmware resident in Trustzone EL3 must implement and conform to the
Power State Coordination Interface specification [PSCI]_.

Platforms without EL3 must implement one of:

- PSCI at EL2 (leaving only EL1 available to an operating system)
- Linux AArch64 spin tables [LINUXA64BOOT]_ (Devicetree only)

However, the spin table protocol is strongly discouraged.
Future versions of this specification will only allow PSCI, and PSCI should
be implemented in all new designs.
