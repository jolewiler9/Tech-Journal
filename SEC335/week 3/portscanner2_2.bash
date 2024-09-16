#!/bin/bash

# ERROR HANDLING
# Check if the correct number of arguments are provided
if [[ $# -ne 2 ]]; then
	echo "Usage $0 <prefix> <port>"
	exit 1
fi


# Assign variables
prefix=$1
port=$2


# OUTPUT ENHANCEMENT
#Output header
echo "Host, Port, Status"


# Create the host addresses and loop through them finding open ports
for i in {1..254}; do
	host="$prefix.$i"
	# Check if the port is open
	timeout 1 bash -c "echo > /dev/tcp/$host/$port" 2>/dev/null
	if [[ $? -eq 0 ]]; then
		echo "$host, $port, Open"
	fi
done
