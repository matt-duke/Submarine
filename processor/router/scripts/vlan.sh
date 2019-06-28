#https://blog.sleeplessbeastie.eu/2012/12/23/debian-how-to-create-vlan-interface/

#internal communication
vconfig add eth0 100
ifconfig eth0.100 192.168.1.1/24

#router network
vconfig add eth0 200
ifconfig eth0.200 192.168.2.1/24


echo "1" > /proc/sys/net/ipv4/ip_forward
iptables -A PREROUTING -t nat -i eth0.200 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.2:5000
#forward all incoming tcp connections on port 80 to MPC port 5000
iptables -A FORWARD -p tcp -d 192.168.2.2 --dport 5000 -j ACCEPT
iptables -A POSTROUTING -t nat -s 192.168.2.2 -o eth0.100 -j MASQUERADE


#https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software
apt-get install hostapd isc-dhcp-server
#edit /etc/dhcp/dhcpd.conf and /etc/network/interfaces as in guide

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
