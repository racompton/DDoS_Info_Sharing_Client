# DDoS Info Sharinig Client
The DDoS Info Sharing Project is a centralized database of DDoS attack source IPs and attack details which is continually contributed by various ASNs that detect DDoS attacks.  Any ASN can contact CableLabs to get an account.  Once an account has been created, the owner of the account can query the RESTful API to retrieve information about what source IPs in that ASN are contributing DDoS attacks.  The abuse group in that ASN can then help remediate the sources generating attack traffic.

This python script retrieves the list of DDoS attacks that occured the last X number of days and writes it to a file (-f), writes it to syslog (-l) or outputs it to the terminal (if -f or -l are not set).
The output of this script is in the CSV format of field1=value1, field2=value2, etc.  The RESTful API by default outputs as JSON.

## Example usage:
get_ddos_info.py -k (key) -u (username) -d (number of days to query) -l (limit results to x, 0 means don't limit) -f (output filename)

## Attack type shows:
### Only Total Traffic
Ignore, could be spoofed traffic (false positive)
### TCP SYN, TCP ACK, TCP RST or TCP Null
Is the "numberOfTimesSeen" > 1?
If not, ignore, could be spoofed (false positive)
If "numberOfTimesSeen" < 1, the customer probably has some device that is infected with botnet malware on a computer (more likely) or IoT device (less likely)
Suggest that the customer run the anti-bot software on all their Windows computers.  Could also be ACK or RST amplification.  See: https://www.usenix.org/system/files/conference/woot14/woot14-kuhrer.pdf  Also could be TCP Middlebox amplifcation attack.  See: https://geneva.cs.umd.edu/posts/usenix21-weaponizing-censors/
### chargen Amplification
Traffic is highly likely not spoofed and customer has an open chargen server (UDP port 19) on a server connected directly to the Internet.  Recommended that the ISP should just block UDP 19 traffic at the edge to stop this type of traffic.
### CLDAP Amplification
Traffic is highly likely not spoofed and customer has an open chargen server (UDP port 389) on a server connected directly to the Internet. Recommended to contact customer and have them disable UDP port 389 on their device (often Microsoft Exchange).
### DNS Amplification
Traffic is highly likely not spoofed and customer has an open DNS server (UDP port 53) on their CPE or, less likely, server connected directly to the Internet.  The CPE needs to have the firmware upgraded or replaced with another device. 
### SSDP Amplification
Traffic is highly likely not spoofed and customer has an open SSDP server (UDP port 1900) on their CPE.  The CPE needs to have the firmware upgraded or replaced with another device.  Recommended to block UDP 1900 source and dest traffic at the edge.  This traffic should only be multicast traffic on the LAN.
### SNMP Amplification
Traffic is highly likely not spoofed and customer has an open SNMP server (UDP port 1900) on their CPE.  The CPE needs to have the default SNMP community strings changed (kind of like the passwords for that SNMP service, the most common ones are 'public' and 'private'), or the firmware needs to be upgraded or replaced with another device.
### NTP Amplification
Traffic is highly likely not spoofed and customer has an open NTP server (UDP port 123) responding to monlist or version requests connected directly to the Internet.   Recommended to contact customer and have them disable responding to monlist or version requests on their NTP server.
https://blog.cloudflare.com/understanding-and-mitigating-ntp-based-ddos-attacks/
It is very less likely that the CPE has an issue and would need to have the firmware upgraded or replaced with another device.  
### Memcached Amplification
Traffic is highly likely not spoofed and customer has an open Memcached server (UDP port 11211) responding to monlist or version requests connected directly to the Internet.   Recommended to contact customer and have them disable UDP Memcached on their server.
https://www.digitalocean.com/community/tutorials/how-to-secure-memcached-by-reducing-exposure
It is very less likely that the CPE has an issue and would need to have the firmware upgraded or replaced with another device.  
### rpcbind Amplification
Traffic is highly likely not spoofed and customer has an open rpcbind server (UDP port 111) responding to requests connected directly to the Internet.  
### mDNS Amplification
Traffic is highly likely not spoofed and customer has an open mDNS server (UDP port 5353) on their CPE or, less likely, server connected directly to the Internet.  The CPE needs to have the firmware upgraded or replaced with another device. Recommended to block UDP 5353 source and dest traffic at the edge.  This traffic should only be multicast traffic on the LAN.
### MS SQL RS Amplification
Traffic is highly likely not spoofed and customer has an open MS SQL server (UDP port 1434) responding to requests connected directly to the Internet. Recommended to contact customer and have them disable UDP port 1434 on their device (MS SQL server).
### NetBIOS Amplification
Traffic is highly likely not spoofed and customer has an open Windows computer with NetBIOS (UDP port 137) responding to requests connected directly to the Internet.
### L2TP Amplification
Traffic is highly likely not spoofed and customer has an open L2TP server (UDP port 1701) responding to requests connected directly to the Internet.
It is very less likely that the CPE has an issue and would need to have the firmware upgraded or replaced with another device.
### RIPv1 Amplification
Traffic is highly likely not spoofed and customer has an open RIPv1 server (UDP port 520) on their CPE.  The CPE needs to have the firmware upgraded or replaced with another device. 
### Only UDP
This could be that the customer has some device that is infected with botnet malware on a computer (more likely) or IoT device (less likely)
Suggest that the customer run the anti-bot software on all their Windows computers, suggest IoT devices be upgraded/secured.
### ICMP
Could be false positive.  Could be from a botnet or could be from an ICMP Directed Broadcast attack (Smurf Attack https://en.wikipedia.org/wiki/Smurf_attack).  Smurf Attacks result from spoofed traffic sent into a network so an indicator that it is a Smurf Attack is that there will be numerous source IPs within the same subnet (business or infrastructure IP space).  Recommended remediation is to have customer/ISP configure "no ip directed-broadcasts" on interfaces.
### IPv4 Protocol 0
Traffic is likely generated by a botnet.  Suggest that the customer run the anti-bot software on all their Windows computers, suggest IoT devices be upgraded/secured.
### memcached
Traffic is highly likely not spoofed and customer has an open memcached server (UDP port 11211) responding to requests connected directly to the Internet.  Recommended to contact customer and have them disable UDP port 11211 on their device.
