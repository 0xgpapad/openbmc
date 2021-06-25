#!/usr/bin/env python
#
# Copyright 2014-present Facebook. All Rights Reserved.
#
# This program file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program in a file named COPYING; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA
#

import os

from aiohttp.web import Application
from compute_rest_shim import RestShim
from node_bios import (
    get_node_bios,
    get_node_bios_boot_order_trunk,
    get_node_bios_postcode_trunk,
    get_node_bios_plat_info_trunk,
    get_node_bios_boot_mode,
    get_node_bios_clear_cmos,
    get_node_bios_force_boot_setup,
    get_node_bios_boot_order,
)
from node_bmc import get_node_bmc
from node_config import get_node_config
from node_fans import get_node_fans
from node_fruid import get_node_fruid
from node_logs import get_node_logs
from node_mezz import get_node_mezz
from node_sensors import get_node_sensors
from node_server import get_node_server
from node_spb import get_node_spb
from redfish_account_service import get_account_service
from redfish_chassis import (
    get_chassis,
    get_chassis_members,
    get_chassis_power,
    get_chassis_thermal,
)
from redfish_managers import (
    get_managers,
    get_managers_members,
    get_manager_ethernet,
    get_ethernet_members,
    get_manager_network,
)
from redfish_service_root import get_redfish, get_service_root
from rest_pal_legacy import pal_is_fru_prsnt, pal_get_num_slots


def populate_server_node(app: Application, num: int):
    prsnt = pal_is_fru_prsnt(num)
    if prsnt is None or prsnt == 0:
        return

    base_route = "/api/server" + repr(num)
    node_server_shim = RestShim(get_node_server(num), base_route)

    app.router.add_get(node_server_shim.path, node_server_shim.get_handler)
    app.router.add_post(node_server_shim.path, node_server_shim.post_handler)

    # Add /api/server(1-n)/fruid
    fruid_path = os.path.join(base_route, "fruid")
    node_fruid_shim = RestShim(get_node_fruid("slot" + repr(num)), fruid_path)
    app.router.add_get(node_fruid_shim.path, node_fruid_shim.get_handler)
    # Add /api/server(1-n)/sensors
    sensors_path = os.path.join(base_route, "sensors")
    node_sensors_shim = RestShim(get_node_sensors("slot" + repr(num)), sensors_path)
    app.router.add_get(node_sensors_shim.path, node_sensors_shim.get_handler)
    app.router.add_post(node_sensors_shim.path, node_sensors_shim.post_handler)
    # Add /api/server(1-n)/logs
    logs_path = os.path.join(base_route, "logs")
    node_logs_shim = RestShim(get_node_logs("slot" + repr(num)), logs_path)
    app.router.add_get(node_logs_shim.path, node_logs_shim.get_handler)
    app.router.add_post(node_logs_shim.path, node_logs_shim.post_handler)
    # Add /api/server(1-n)/config
    config_path = os.path.join(base_route, "config")
    node_config_shim = RestShim(get_node_config("slot" + repr(num)), config_path)
    app.router.add_get(node_config_shim.path, node_config_shim.get_handler)
    app.router.add_post(node_config_shim.path, node_config_shim.post_handler)

    # Add /api/server(1-n)/bios
    bios_path = os.path.join(base_route, "bios")
    node_bios_shim = RestShim(get_node_bios("server" + repr(num)), bios_path)
    app.router.add_get(node_bios_shim.path, node_bios_shim.get_handler)

    # Add /api/server(1-n)/bios/boot-order
    boot_order_trunk_path = os.path.join(base_route, "bios", "boot-order")
    boot_order_trunk_shim = RestShim(
        get_node_bios_boot_order_trunk("slot" + repr(num)),
        boot_order_trunk_path,
    )
    app.router.add_get(boot_order_trunk_shim.path, boot_order_trunk_shim.get_handler)

    # Add /api/server(1-n)/bios/postcode
    postcode_path = os.path.join(base_route, "bios", "postcode")
    postcode_shim = RestShim(
        get_node_bios_postcode_trunk("slot" + repr(num)),
        postcode_path,
    )
    app.router.add_get(postcode_shim.path, postcode_shim.get_handler)

    # Add /api/server(1-n)/bios/plat-info
    platinfo_path = os.path.join(base_route, "bios", "plat-info")
    platinfo_shim = RestShim(
        get_node_bios_plat_info_trunk("slot" + repr(num)),
        platinfo_path,
    )
    app.router.add_get(platinfo_shim.path, platinfo_shim.get_handler)
    # Add /api/server(1-n)/bios/boot-order/boot_mode
    bootmode_path = os.path.join(base_route, "bios", "boot-order", "boot_mode")
    bootmode_shim = RestShim(
        get_node_bios_boot_mode("slot" + repr(num)),
        bootmode_path,
    )
    app.router.add_get(bootmode_shim.path, bootmode_shim.get_handler)
    app.router.add_post(bootmode_shim.path, bootmode_shim.post_handler)
    # Add /api/server(1-n)/bios/boot-order/clear_cmos
    clear_cmos_path = os.path.join(base_route, "bios", "boot-order", "clear_cmos")
    clear_cmos_shim = RestShim(
        get_node_bios_clear_cmos("slot" + repr(num)),
        clear_cmos_path,
    )
    app.router.add_get(clear_cmos_shim.path, clear_cmos_shim.get_handler)
    app.router.add_post(clear_cmos_shim.path, clear_cmos_shim.post_handler)
    # Add /api/server(1-n)/bios/boot-order/force_boot_bios_setup
    force_boot_bios_setup_path = os.path.join(
        base_route, "bios", "boot-order", "force_boot_bios_setup"
    )
    force_boot_bios_setup_shim = RestShim(
        get_node_bios_force_boot_setup("slot" + repr(num)),
        force_boot_bios_setup_path,
    )
    app.router.add_get(
        force_boot_bios_setup_shim.path, force_boot_bios_setup_shim.get_handler
    )
    app.router.add_post(
        force_boot_bios_setup_shim.path, force_boot_bios_setup_shim.post_handler
    )
    # Add /api/server(1-n)/bios/boot-order/boot_order
    boot_order_path = os.path.join(base_route, "bios", "boot-order", "boot_order")
    boot_order_shim = RestShim(
        get_node_bios_boot_order("slot" + repr(num)),
        boot_order_path,
    )
    app.router.add_get(boot_order_shim.path, boot_order_shim.get_handler)
    app.router.add_post(boot_order_shim.path, boot_order_shim.post_handler)


# Initialize Platform specific Resource Tree
def setup_board_routes(app: Application, write_enabled: bool):

    # Add /api/spb to represent side plane board
    spb_shim = RestShim(get_node_spb(), "/api/spb")
    app.router.add_get(spb_shim.path, spb_shim.get_handler)
    app.router.add_post(spb_shim.path, spb_shim.post_handler)
    # Add /api/mezz to represent Network Mezzaine card
    mezz_shim = RestShim(get_node_mezz(), "/api/mezz")
    app.router.add_get(mezz_shim.path, mezz_shim.get_handler)

    # Add servers /api/server[1-max]
    num = pal_get_num_slots()
    for i in range(1, num + 1):
        populate_server_node(app, i)

    # Add /api/spb/fruid end point
    spb_fruid_shim = RestShim(get_node_fruid("bmc"), "/api/spb/fruid")
    app.router.add_get(spb_fruid_shim.path, spb_fruid_shim.get_handler)
    # /api/spb/bmc end point
    spb_bmc_shim = RestShim(get_node_bmc(), "/api/spb/bmc")
    app.router.add_get(spb_bmc_shim.path, spb_bmc_shim.get_handler)
    app.router.add_post(spb_bmc_shim.path, spb_bmc_shim.post_handler)
    # /api/spb/sensors end point
    spb_sensors_shim = RestShim(get_node_sensors("bmc"), "/api/spb/sensors")
    app.router.add_get(spb_sensors_shim.path, spb_sensors_shim.get_handler)
    app.router.add_post(spb_sensors_shim.path, spb_sensors_shim.post_handler)
    # Add /api/spb/fans end point
    spb_fans_shim = RestShim(get_node_fans(), "/api/spb/fans")
    app.router.add_get(spb_fans_shim.path, spb_fans_shim.get_handler)
    # /api/spb/logs end point
    spb_logs_shim = RestShim(get_node_logs("bmc"), "/api/spb/logs")
    app.router.add_get(spb_logs_shim.path, spb_logs_shim.get_handler)
    app.router.add_post(spb_logs_shim.path, spb_logs_shim.post_handler)

    # Add /api/mezz/fruid end point
    nic_fruid_shim = RestShim(get_node_fruid("nic"), "/api/mezz/fruid")
    app.router.add_get(nic_fruid_shim.path, nic_fruid_shim.get_handler)
    # /api/mezz/sensors end point
    nic_sensors_shim = RestShim(get_node_sensors("nic"), "/api/mezz/sensors")
    app.router.add_get(nic_sensors_shim.path, nic_sensors_shim.get_handler)
    app.router.add_post(nic_sensors_shim.path, nic_sensors_shim.post_handler)
    # /api/mezz/logs end point
    nic_logs_shim = RestShim(get_node_logs("nic"), "/api/mezz/logs")
    app.router.add_get(nic_logs_shim.path, nic_logs_shim.get_handler)
    app.router.add_post(nic_logs_shim.path, nic_logs_shim.post_handler)

    # /redfish end point
    redfish_shim = RestShim(get_redfish(), "/redfish")
    app.router.add_get(redfish_shim.path, redfish_shim.get_handler)
    # /redfish/v1 end point
    service_root_shim = RestShim(get_service_root(), "/redfish/v1")
    app.router.add_get(service_root_shim.path, service_root_shim.get_handler)
    # /redfish/v1/AccountService end point
    account_service_shim = RestShim(get_account_service(), "/redfish/v1/AccountService")
    app.router.add_get(account_service_shim.path, account_service_shim.get_handler)
    # /redfish/v1/Chassis end point
    chassis_shim = RestShim(get_chassis(), "/redfish/v1/Chassis")
    app.router.add_get(chassis_shim.path, chassis_shim.get_handler)
    # /redfish/v1/Chassis/1 end point
    chassis_1_shim = RestShim(get_chassis_members("bmc"), "/redfish/v1/Chassis/1")
    app.router.add_get(chassis_1_shim.path, chassis_1_shim.get_handler)
    # /redfish/v1/Chassis/1/Power end point
    chassis_power_shim = RestShim(
        get_chassis_power("bmc", "BMC_SENSOR_HSC_PIN", "0xF9"),
        "/redfish/v1/Chassis/1/Power",
    )
    app.router.add_get(chassis_power_shim.path, chassis_power_shim.get_handler)
    # /redfish/v1/Chasis/1/Thermal end point
    chassis_thermal_shim = RestShim(
        get_chassis_thermal("bmc"), "/redfish/v1/Chassis/1/Thermal"
    )
    app.router.add_get(chassis_thermal_shim.path, chassis_thermal_shim.get_handler)

    # /redfish/v1/Managers end point
    manager_shim = RestShim(get_managers(), "/redfish/v1/Managers")
    app.router.add_get(manager_shim.path, manager_shim.add_get)
    # /redfish/v1/Managers/1 end point
    manager_member_shim = RestShim(get_managers_members(), "/redfish/v1/Managers/1")
    app.router.add_get(manager_member_shim.path, manager_member_shim.get_handler)
    # /redfish/v1/Managers/1/EthernetInterfaces end point
    manager_ethernet_shim = RestShim(
        get_manager_ethernet(),
        "/redfish/v1/Managers/1/EthernetInterfaces",
    )
    app.router.add_get(manager_ethernet_shim.path, manager_ethernet_shim.get_handler)
    # /redfish/v1/Managers/1/NetworkProtocol end point
    manager_network_shim = RestShim(
        get_manager_network(),
        "/redfish/v1/Managers/1/NetworkProtocol",
    )
    app.router.add_get(manager_network_shim.path, manager_network_shim.get_handler)
    # /redfish/v1/Managers/1/EthernetInterfaces/1 end point
    ethernet_members_shim = RestShim(
        get_ethernet_members(),
        "/redfish/v1/Managers/1/EthernetInterfaces/1",
    )
    app.router.add_get(ethernet_members_shim.path, ethernet_members_shim.get_handler)
