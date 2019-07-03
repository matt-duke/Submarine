import common
import core


import os
from configparser import ConfigParser

def update_dict(new, default):
    for key, item in default:
        if sum([default[key] == item for key, item in new.items()]):
            break
        new[key] = item
    return default

class NetController(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self)
        
    def configure_network(self):
        default = common.defaults.get()
        networking = default['networking']
        for ntwrk in ['internal', 'public']:
            dev = networking[ntwrk]['dev']
            vlan = networking[ntwrk]['vlan']
            ip = networking[ntwrk]['ip']
            self.systemCall('vconfig add {} {}'.format(dev, vlan))
            self.systemCall('ifconfig {}.{} {}'.format(dev, vlan, ip))
    
        with open('/proc/sys/net/ipv4/ip_forward', 'a') as file:
            file.write('1')
        
        webgui_settings = networking['applications']['webgui']
        webgui_network = networking[webgui_settings['network']]
        # Route rules for client to GUI
        self.systemCall('iptables -A PREROUTING -t nat -i {}.{} -p tcp --dport {} -j DNAT --to-destination {}:{}'.format(
            webgui_network['dev'],
            webgui_network['vlan'],
            webgui_settings['external_port'],
            webgui_network['mpc_ip'],
            webgui_settings['internal_port']
        ))
        self.systemCall('iptables -A FORWARD -p tcp -d {} --dport {} -j ACCEPT'.format(
            webgui_network['mpc_ip'],
            webgui_settings['port']
        ))
        self.systemCall('iptables -A POSTROUTING -t nat -s {} -o {}.{} -j MASQUERADE'.format(
            webgui_network['mpc_ip'],
            webgui_network['dev'],
            webgui_network['vlan'] 
        ))   
    
    def enable_ap(self):
        self.disable_ap()
        
        wifi_ap = common.defaults.get()['networking']['applications']['wifi_ap']
        dnsmasq_file = os.path.join(common.Paths['DATABASE'], 'dnsmasq.conf'
        file = '[DEFAULT]\n'+open(dnsmasq_file, 'r')
        dnsmasq = ConfigParser.read(file)
        dnsmasq_default = {'interface', networking[wifi_ap['network']],
                           'dhcp-range': '{},{},255.255.255.0,24h'.format(
                               wifi_ap['dhcp_start'],
                               wifi_ap['dhcp_end']
                               )}
                               
        dnsmasq = update_dict(dnsmasq_default, dnsmasq)
                
        with open(dnsmasq_file, 'w') as file:
            dnsmasq.write(file)

        hostapd_file = os.path.join(common.Paths['DATABASE'], 'hostapd.conf'
        file = '[DEFAULT]\n'+open(hostapd_file, 'r')
        hostapd = ConfigParser.read(file)
        hostapd_default = {'interface', networking[wifi_ap['network']],
                           'ssid': common.CVT.wifi.ssid,
                           'wpa_passphrase': common.CVT.wifi.key
                          }
                               
        hostapd = update_dict(hostapd_default, hostapd)
                
        with open(hostapd_file, 'w') as file:
            hostapd.write(file)
            
        #SETUP DONE    
        self.systemCall('service hostapd start')
        
    def disable_ap(self):
        self.systemCall('service hostapd stop')