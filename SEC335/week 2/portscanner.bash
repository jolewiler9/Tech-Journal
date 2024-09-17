#!/bin/bash

# ERROR HANDLING
# Check if the correct number of arguments are provided
if [[ $# -ne 2 ]]; then
	echo "Usage $0 <hostfile> <portfile>"
	exit 1
fi


# Assign variables
hostfile=$1
portfile=$2


# Check if hostfile exists and is readable
if [[ ! -f "$hostfile" || ! -r "$hostfile" ]]; then
	echo "Error: Cannot read hostfile '$hostfile'"
	exit 1
fi


# Check if portfile exists and is readable
if [[ ! -f "$portfile" || ! -r "$portfile" ]]; then
	echo "Error: Cannot read portfile '$portfile'"
	exit 1
fi


# OUTPUT ENHANCEMENT
#Output header
echo "Host, Port, Status"


# Loop through hosts and ports in files, while utilizing error handling
# and refining output
for host in $(cat "$hostfile"); do
	open_ports="" # Use a string to store open ports
	for port in $(cat "$portfile"); do
		# Check if the port is open
		timeout 1 bash -c "echo > /dev/tcp/$host/$port" 2>/dev/null
		if [[ $? -eq 0 ]]; then
			open_ports+="$port " # Add the open port to the string
		fi
	done

	# Print the open ports
	if [[ -n "$open_ports" ]]; then
		echo "$host, $open_ports"
	fi
done

