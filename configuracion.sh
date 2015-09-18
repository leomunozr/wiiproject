#!/usr/bin/env 	bash

###############################################
## Script para instalar las herramientas I2C ##
## y configurar la Raspberry Pi para su uso  ##
##                                           ##
## Leonardo Muñoz                            ##
###############################################

# Revisa si tiene permisos de administrador

if [ "$(whoami)" != "root" ]; then
	echo "Must run as root."
	exit 1
fi

echo "Installing modules..."

# Instala los módulos y herramientas I2C
apt-get install -y python-smbus
apt-get install -y i2c-tools
apt-get install -y python-dev
apt-get install -y python-rpi.gpio

echo "Modules installed."

echo "Configuring modules..."

# Agrega los módulos a /etc/modules si no existen ya
grep -q "i2c-bcm2708" /etc/modules || echo "i2c-bcm2708" >> /etc/modules
grep -q "i2c-dev" /etc/modules || echo "i2c-dev" >> /etc/modules

sed -i '/blacklist spi-bcm2708/c\#blacklist spi-bcm2708' /etc/modprobe.d/raspi-blacklist.conxf
sed -i '/blacklist i2c-bcm2708/c\#blacklist i2c-bcm2708' /etc/modprobe.d/raspi-blacklist.conf

grep -q "dtparam=i2c1=on" /etc/modules || echo "dtparam=i2c1=on" >> /boot/config.txt
grep -q "dtparam=i2c_arm=on" /etc/modules || echo "dtparam=i2c_arm=on" >> /boot/config.txt

echo "Done!"

read -p "Reboot now? [y/n] " choice
if [ "$choice" == "y" ]; then
	echo "Rebooting now"
	reboot
else
	echo "Done!"
fi
