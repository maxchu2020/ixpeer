#! /usr/local/bin/python3.10

import paramiko
import time
import getpass
import sys

username = input('Username: ')
password = getpass.getpass('Password: ')

asn_description = sys.argv[1]
asn = sys.argv[2]
prefix_limit_v4 = sys.argv[3]
prefix_limit_v6 = sys.argv[4]
ix = sys.argv[5]
ip_v4 = sys.argv[6]
ip_v6 = sys.argv[7]

if ix == "sgix":
        host = '156.248.72.2'
        ix_name = "SGIX"
        set_neighbor_v4 = "set routing-instances SGIX protocols bgp group bg_EBGP-SGIX-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances SGIX protocols bgp group bg_EBGP-SGIX-PEER_v6 neighbor "

elif ix == "eie-sg":
        host = '156.248.72.2'
        ix_name = "EIE-SG"
        set_neighbor_v4 = "set routing-instances EIE-SG protocols bgp group bg_EBGP-EIE-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances EIE-SG protocols bgp group bg_EBGP-EIE-PEER_v6 neighbor "

elif ix == "bbix-sg":
        host = '156.248.72.2'
        ix_name = "BBIX-SG"
        set_neighbor_v4 = "set protocols bgp group bg_EBGP-BBIX-PEER_v4 neighbor "
        set_neighbor_v6 = "set protocols bgp group bg_EBGP-BBIX-PEER_v6 neighbor "

elif ix == "eie-hk":
        host = '156.248.72.8'
        ix_name = "EIE-HK"
        set_neighbor_v4 = "set routing-instances EIE-HK protocols bgp group bg_EBGP-EIE-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances EIE-HK protocols bgp group bg_EBGP-EIE-PEER_v6 neighbor "

elif ix == "bbix-hk":
        host = '156.248.72.4'
        ix_name = "BBIX-HK"
        set_neighbor_v4 = "set routing-instances BBIX-HK protocols bgp group bg_EBGP-BBIX-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances BBIX-HK protocols bgp group bg_EBGP-BBIX-PEER_v6 neighbor "

elif ix == "tpix":
        host = '156.248.72.3'
        ix_name = "TPIX"
        set_neighbor_v4 = "set routing-instances TPIX protocols bgp group bg_EBGP-TPIX-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances TPIX protocols bgp group bg_EBGP-TPIX-PEER_v6 neighbor "

elif ix == "eie-ty":
        host = '156.248.72.7'
        ix_name = "EIE-TY"
        set_neighbor_v4 = "set routing-instances EIE-TY protocols bgp group bg_EBGP-EIE-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances EIE-TY protocols bgp group bg_EBGP-EIE-PEER_v6 neighbor "

elif ix == "bbix-ty":
        host = '156.248.72.7'
        ix_name = "BBIX-TY"
        set_neighbor_v4 = "set routing-instances BBIX-TY protocols bgp group bg_EBGP-BBIX-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances BBIX-TY protocols bgp group bg_EBGP-BBIX-PEER_v6 neighbor "

elif ix == "eie-sv":
        host = '156.248.72.11'
        ix_name = "EIE-SV"
        set_neighbor_v4 = "set routing-instances EIE-SV protocols bgp group bg_EBGP-EIE-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances EIE-SV protocols bgp group bg_EBGP-EIE-PEER_v6 neighbor "

elif ix == "bbix-sv":
        host = '156.248.72.10'
        ix_name = "BBIX-SV"
        set_neighbor_v4 = "set routing-instances BBIX-SV protocols bgp group bg_EBGP-BBIX-PEER_v4 neighbor "
        set_neighbor_v6 = "set routing-instances BBIX-SV protocols bgp group bg_EBGP-BBIX-PEER_v6 neighbor "

else:
        print("what ix?\n")

print(" ")
print("IX = " + ix_name)
print("ORG = " + asn_description)
print("ASN = " + asn)
print("IPv4 Prefix Limit = " + prefix_limit_v4)
print("IPv6 Prefix Limit = " + prefix_limit_v6)
print("IPv4 = " + ip_v4)
print("IPv6 = " + ip_v6)
print(" ")

ip = host
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
print("Successfully connect to ", ip)

command = ssh_client.invoke_shell()
command.send("edit\n")
command.send(set_neighbor_v4 + ip_v4 + " description " + asn_description + "\n")
time.sleep(1)
command.send(set_neighbor_v4 + ip_v4 + " family inet unicast prefix-limit maximum " + prefix_limit_v4 + "\n")
time.sleep(1)
command.send(set_neighbor_v4 + ip_v4 + " family inet unicast prefix-limit teardown idle-timeout 20\n")
time.sleep(1)
command.send(set_neighbor_v4 + ip_v4 + " peer-as " + asn + "\n")
time.sleep(1)
command.send(set_neighbor_v6 + ip_v6 + " description " + asn_description + "\n")
time.sleep(1)
command.send(set_neighbor_v6 + ip_v6 + " family inet6 unicast prefix-limit maximum " + prefix_limit_v6 + "\n")
time.sleep(1)
command.send(set_neighbor_v6 + ip_v6 + " family inet6 unicast prefix-limit teardown idle-timeout 20\n")
time.sleep(1)
command.send(set_neighbor_v6 + ip_v6 + " peer-as " + asn + "\n")
time.sleep(1)

command.send("commit and-quit\n")
time.sleep(10)
output = command.recv(65535)
print(output.decode('ascii'))

command.send("show bgp summary | match " + asn + "\n")
time.sleep(10)
output = command.recv(65535)
print(output.decode('ascii'))

ssh_client.close

# ./ixpeer.2.py CLOUDFLARE 13335 20000 2000 bbix-sv 101.203.74.14 2403:c780:7200:b074:0:1:3335:1
