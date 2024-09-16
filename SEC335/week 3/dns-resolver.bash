#!/bin/bash

# ERROR HANDLING
# Check if the correct number of arguments are provided
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <network_prefix> <dns_server>"
    exit 1
fi

# Assign variables
network_prefix=$1
dns_server=$2

# Output header
echo "Performing nslookup on $network_prefix.0/24 using DNS server $dns_server"
echo "IP Address, Lookup Result"

# Loop through the IP addresses in the network
for host in {1..254}; do
    # Construct the full IP
    ip="$network_prefix.$host"

    # Perform nslookup using the specified DNS server
    lookup_result=$(nslookup $ip $dns_server 2>/dev/null | grep 'name =')
    
    # If there is a result, print it
    if [[ -n "$lookup_result" ]]; then
        echo "$ip, $lookup_result"
    fi
done
