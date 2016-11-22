#!/bin/bash

export PATH=/sbin/:/bin/:/usr/sbin:/usr/bin:$PATH

echo "ZTE VPN LINUX CONNECT SCRIPT:"
#read -p "Please input you ZTE VPN account: " USERNAME
USERNAME=10117906

if [ -z "$USERNAME" ] ; then
echo "ERROR: no VPN Account, exit. VPN account is 7 digit ID."
exit 1
fi

#read -s -p "Please input $USERNAME 's Password: " PASSWORD
PASSWORD=zkm0.12345

if [ -z "$PASSWORD" ] ; then
echo "ERROR: no VPN Password, exit. VPN password is ZTE domain login password."
exit 1
fi

killall wpa_supplicant 2>/dev/null
ifdown  enp2s0 2>/dev/null

(
cat <<EOF

ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=root
ap_scan=0
network={
   key_mgmt=IEEE8021X
   eap=PEAP
   phase1="peaplabel=0"
   phase2="auth=GTC"
   identity="$USERNAME"
   password="$PASSWORD"
}
EOF
) > /tmp/wpa_supplicant.conf

wpa_supplicant  -d -B -i enp2s0 -c /tmp/wpa_supplicant.conf -D wired

rm -f /tmp/wpa_supplicant.conf

echo "up enp2s0"
ifup    enp2s0
sleep 3
dhclient enp2s0


