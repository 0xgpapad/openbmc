#
# Copyright 2020-present Facebook. All Rights Reserved.
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

FILESEXTRAPATHS:prepend := "${THISDIR}/files/pal:"

SRC_URI += " \
    file://plat/meson.build \
    file://pal-pim.c \
    file://pal-pim.h \
    file://pal_debugcard.c \
    file://pal_debugcard.h \
    file://pal_power.c \
    file://pal_power.h \
    file://pal_sensors.c \
    file://pal_sensors.h \
    file://pal.c \
    file://pal.h \
    "

DEPENDS += " \
    libbic \
    libgpio-ctrl \
    liblog \
    libmisc-utils \
    libobmc-i2c \
    libsensor-correction \
    libwedge-eeprom \
    "

# These shouldn't be needed but are because we aren't properly versioning the
# shared libraries contained in these recipes.
RDEPENDS:${PN} += " \
    libbic \
    libgpio-ctrl \
    liblog \
    libmisc-utils \
    libobmc-i2c \
    libsensor-correction \
    libwedge-eeprom \
    "
