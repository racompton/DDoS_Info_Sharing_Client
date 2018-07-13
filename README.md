# DDoS Info Sharinig Client
The DDoS Info Sharing Project is a centralized database of DDoS attack source IPs and attack details which is continually contributed by various ASNs that detect DDoS attacks.  Any ASN can contact CableLabs to get an account.  Once an account has been created, the owner of the account can query the RESTful API to retrieve information about what source IPs in that ASN are contributing DDoS attacks.  The abuse group in that ASN can then help remediate the sources generating attack traffic.

This python script retrieves the list of DDoS attacks that occured the last X number of days and writes it to a file (-f), writes it to syslog (-l) or outputs it to the terminal (if -f or -l are not set).
The output of this script is in the CEF format of field1=value1, field2=value2, etc.  The RESTful API by default outputs as JSON.

## Example usage:
get_ddos_info.py -k <key> -u <username> -d <number of days to query> -l <limit results to x, 0 means don't limit> -f <output filename>

## Attack type shows:
### Only Total Traffic
Ignore, could be spoofed traffic (false positive)
### TCP SYN or TCP RST or TCP Null
Is the "numberOfTimesSeen" > 1?
If not, ignore, could be spoofed (false positive)
If "numberOfTimesSeen" < 1, the customer probably has some device that is infected with botnet malware on a computer (more likely) or IoT device (less likely)
Suggest that the customer run the anti-bot software on all their Windows computers
### DNS Amplification
Traffic is highly likely not spoofed and customer has an open DNS server (UDP port 53) on their CPE or, less likely, server connected directly to the Internet.  The CPE needs to have the firmware upgraded or replaced with another device. 
### SSDP Amplification
Traffic is highly likely not spoofed and customer has an open SSDP server (UDP port 1900) on their CPE.  The CPE needs to have the firmware upgraded or replaced with another device.
### SNMP Amplification
Traffic is highly likely not spoofed and customer has an open SNMP server (UDP port 1900) on their CPE.  The CPE needs to have the default SNMP community strings changed (kind of like the passwords for that SNMP service, the most common ones are public/private), or the firmware needs to be upgraded or replaced with another device.
### NTP Amplification
Traffic is highly likely not spoofed and customer has an open NTP server (UDP port 123) responding to monlist requests connected directly to the Internet.  
https://blog.cloudflare.com/understanding-and-mitigating-ntp-based-ddos-attacks/
It is very less likely that the CPE has an issue and would need to have the firmware upgraded or replaced with another device.
### chargen Amplification
Traffic is highly likely not spoofed and customer has an open chargen server (UDP port 19) responding to requests connected directly to the Internet.  
### rpcbind Amplification
Traffic is highly likely not spoofed and customer has an open rpcbind server (UDP port 111) responding to requests connected directly to the Internet.  
### mDNS Amplification
Traffic is highly likely not spoofed and customer has an open mDNS server (UDP port 5353) on their CPE or, less likely, server connected directly to the Internet.  The CPE needs to have the firmware upgraded or replaced with another device. 
### MS SQL RS Amplification
Traffic is highly likely not spoofed and customer has an open MS SQL server (UDP port 1434) responding to requests connected directly to the Internet.
### NetBIOS Amplification
Traffic is highly likely not spoofed and customer has an open Windows computer with NetBIOS (UDP port 137) responding to requests connected directly to the Internet.
### L2TP Amplification
Traffic is highly likely not spoofed and customer has an open L2TP server (UDP port 1701) responding to requests connected directly to the Internet.
It is very less likely that the CPE has an issue and would need to have the firmware upgraded or replaced with another device.
### RIPv1 Amplification
Traffic is highly likely not spoofed and customer has an open RIPv1 server (UDP port 520) on their CPE.  The CPE needs to have the firmware upgraded or replaced with another device. 
### IP Fragmentation and UDP
Traffic is highly likely not spoofed and customer has an open LDAP server (UDP port 389) or an open memcache server (UDP port 11211) responding to requests connected directly to the Internet.
### Only UDP
This could be that the customer has some device that is infected with botnet malware on a computer (more likely) or IoT device (less likely)
Suggest that the customer run the anti-bot software on all their Windows computers, suggest IoT devices be upgraded/secured
