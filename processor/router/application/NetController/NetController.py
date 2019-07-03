import common
import core


class NetController(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self)
        
    def configure_forwarding(self):
        with open('/proc/sys/net/ipv4/ip_forward', 'a') as file:
            file.write('1')
        self.systemCall('iptables -A PREROUTING -t nat -i {} -p tcp --dport {} -j DNAT --to-destination {}:{}')
        self.systemCall('iptables -A FORWARD -p tcp -d {} --dport {} -j ACCEPT')
        self.systemCall('iptables -A POSTROUTING -t nat -s {} -o (} -j MASQUERADE')
        
    def configure_wan(self):
        self.systemCall('iptables -t nat -A POSTROUTING -o {} -j MASQUERADE')
        self.systemCall('iptables -A FORWARD -i {} -o {} -m state --state RELATED,ESTABLISHED -j ACCEPT')
        self.systemCall('iptables -A FORWARD -i {} -o {} -j ACCEPT')
        
    def enable_wan(self):
        self.systemCall('service hostapd start')
        
    def disable_wan(self):
        self.systemCall('service hostapd stop')