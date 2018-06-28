#############################################
APPENDIX A - UEFI Implementation Requirements
#############################################

Required Boot Services
**********************

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_RAISE_TPL                              7.1
EFI_RESTORE_TPL                            7.1
EFI_ALLOCATE_PAGES                         7.2
EFI_FREE_PAGES                             7.2
EFI_GET_MEMORY_MAP                         7.2
EFI_ALLOCATE_POOL                          7.2
EFI_FREE_POOL                              7.2
EFI_CREATE_EVENT                           7.1
EFI_SET_TIMER                              7.1
EFI_WAIT_FOR_EVENT                         7.1
EFI_SIGNAL_EVENT                           7.1
EFI_CLOSE_EVENT                            7.1
EFI_INSTALL_PROTOCOL_INTERFACE             7.3
EFI_REINSTALL_PROTOCOL_INTERFACE           7.3
EFI_UNINSTALL_PROTOCOL_INTERFACE           7.3
EFI_HANDLE_PROTOCOL                        7.3
EFI_REGISTER_PROTOCOL_NOTIFY               7.3
EFI_LOCATE_HANDLE                          7.3
EFI_LOCATE_PROTOCOL                        7.3
EFI_LOCATE_DEVICE_PATH                     7.3
EFI_INSTALL_CONFIGURATION_TABLE            7.3
EFI_IMAGE_LOAD                             7.4
EFI_IMAGE_START                            7.4
EFI_EXIT                                   7.4
EFI_IMAGE_UNLOAD                           7.4
EFI_EXIT_BOOT_SERVICES                     7.4
EFI_GET_NEXT_MONOTONIC_COUNT               7.5
EFI_STALL                                  7.5
EFI_SET_WATCHDOG_TIMER                     7.5
EFI_CONNECT_CONTROLLER                     7.3
EFI_DISCONNECT_CONTROLLER                  7.3
EFI_OPEN_PROTOCOL                          7.3
EFI_CLOSE_PROTOCOL                         7.3
EFI_OPEN_PROTOCOL_INFORMATION              7.3
EFI_PROTOCOLS_PER_HANDLE                   7.3
EFI_LOCATE_HANDLE_BUFFER                   7.3
EFI_LOCATE_PROTOCOL                        7.3
EFI_INSTALL_MULTIPLE_PROTOCOL_INTERFACES   7.3
EFI_UNINSTALL_MULTIPLE_PROTOCOL_INTERFACES 7.3
EFI_CALCULATE_CRC32                        7.5
EFI_COPY_MEM                               7.5
EFI_SET_MEM                                7.5
EFI_CREATE_EVENT_EX                        7.5
========================================== ======

Required Runtime Services
*************************

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_GET_TIME                               8.3
EFI_SET_TIME                               8.3
EFI_GET_WAKEUP_TIME                        8.3
EFI_SET_WAKEUP_TIME                        8.3
EFI_SET_VIRTUAL_ADDRESS_MAP                8.4
EFI_CONVERT_POINTER                        8.4
EFI_GET_VARIABLE                           8.2
EFI_GET_NEXT_VARIABLE_NAME                 8.2
EFI_SET_VARIABLE                           8.2
EFI_GET_NEXT_HIGH_MONO_COUNT               8.5
EFI_RESET_SYSTEM                           8.5
EFI_UPDATE_CAPSULE                         8.5
EFI_QUERY_CAPSULE_CAPABILITIES             8.5
EFI_QUERY_VARIABLE_INFO                    8.5
========================================== ======

.. note:: EFI_GET_WAKEUP_TIME and EFI_SET_WAKEUP_TIME must be implemented, but
   might simply return EFI_UNSUPPORTED.

Required UEFI Protocols
***********************

Core UEFI Protocols
===================

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_LOADED_IMAGE_PROTOCOL                  9.1
EFI_LOADED_IMAGE_DEVICE_PATH_PROTOCOL      9.2
EFI_DECOMPRESS_PROTOCOL                    19.5
EFI_DEVICE_PATH_PROTOCOL                   10.2
EFI_DEVICE_PATH_UTILITIES_PROTOCOL         10.3
========================================== ======

Media I/O Protocols
===================

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_LOAD_FILE2_PROTOCOL                    13.2
EFI_SIMPLE_FILE_SYSTEM_PROTOCOL            13.4
EFI_FILE_PROTOCOL                          13.5
========================================== ======

Console Protocols
=================

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_SIMPLE_TEXT_INPUT_PROTOCOL             12.2
EFI_SIMPLE_TEXT_INPUT_EX_PROTOCOL          12.3
EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL            12.4
========================================== ======

Driver Configuration Protocols
==============================

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_HII_DATABASE_PROTOCOL                  33.4
EFI_HII_STRING_PROTOCOL                    33.4
EFI_HII_CONFIG_ROUTING_PROTOCOL            33.4
EFI_HII_CONFIG_ACCESS_PROTOCOL             33.4
========================================== ======

Optional UEFI Protocols
***********************

Basic Networking Support
========================

============================================ ======
Service                                      UEFI §
============================================ ======
EFI_SIMPLE_NETWORK_PROTOCOL                  24.1
EFI_MANAGED_NETWORK_PROTOCOL                 25.1
EFI_MANAGED_NETWORK_SERVICE_BINDING_PROTOCOL 25.1
============================================ ======

.. note:: Networking services are optional on platforms that do not support
   networking.

Network Boot Protocols
======================

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_PXE_BASE_CODE_PROTOCOL                 24.3
EFI_PXE_BASE_CODE_CALLBACK_PROTOCOL        24.4
EFI_BIS_PROTOCOL                           24.5
EFI_MTFTP4_PROTOCOL                        30.3
EFI_MTFTP6_PROTOCOL                        30.4
========================================== ======

.. note:: EFI_BIS_PROTOCOL is optional on machines that do not support Secure
   Boot.

IPV4 Network Support
====================

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_ARP_PROTOCOL                           29.1
EFI_ARP_SERVICE_BINDING_PROTOCOL           29.1
EFI_DHCP4_SERVICE_BINDING_PROTOCOL         29.2
EFI_DHCP4_PROTOCOL                         29.2
EFI_TCP4_PROTOCOL                          28.1.2
EFI_TCP4_SERVICE_BINDING_PROTOCOL          28.1.1
EFI_IP4_SERVICE_BINDING_PROTOCOL           28.3.1
EFI_IP4_CONFIG2_PROTOCOL                   28.5
EFI_UDP4_PROTOCOL                          30.1.2
EFI_UDP4_SERVICE_BINDING_PROTOCOL          30.1.1
========================================== ======

.. note:: Networking services are optional on platforms that do not support
   networking.

IPV6 Network Support
====================

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_DHCP6_PROTOCOL                         29.3.2
EFI_DHCP6_SERVICE_BINDING_PROTOCOL         29.3.1
EFI_TCP6_PROTOCOL                          28.2.2
EFI_TCP6_SERVICE_BINDING_PROTOCOL          28.2.1
EFI_IP6_SERVICE_BINDING_PROTOCOL           28.6.1
EFI_IP6_CONFIG_PROTOCOL                    28.7
EFI_UDP6_PROTOCOL                          30.2.2
EFI_UDP6_SERVICE_BINDING_PROTOCOL          30.2.1
========================================== ======

.. note:: Networking services are optional on platforms that do not support
   networking.

VLAN Protocols
==============

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_VLAN_CONFIG_PROTOCOL                   27.1
========================================== ======

iSCSI Protocols
===============

========================================== ======
Service                                    UEFI §
========================================== ======
EFI_ISCSI_INITIATOR_NAME_PROTOCOL          16.2
========================================== ======

.. note:: Support for iSCSI is only required on machines that lack persistent
   storage, such as a, HDD. This configuration is intended for thin clients and
   compute-only nodes

