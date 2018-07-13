# DDoS Info Sharinig Client
The DDoS Info Sharing Project is a centralized database of DDoS attack source IPs and attack details which is continually contributed by various ASNs that detect DDoS attacks.  Any ASN can contact CableLabs to get an account.  Once an account has been created, the owner of the account can query the RESTful API to retrieve information about what source IPs in that ASN are contributing DDoS attacks.  The abuse group in that ASN can then help remediate the sources generating attack traffic.

This python script retrieves the list of DDoS attacks that occured the last X number of days and writes it to a file (-f), writes it to syslog (-l) or outputs it to the terminal (if -f or -l are not set).
The output of this script is in the CEF format of <field1>=<value1>, <field2>=<value2>, etc.  The RESTful API by default outputs as JSON.
