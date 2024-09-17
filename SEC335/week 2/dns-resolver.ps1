# dns-resolver.ps1

param($Dns, $Prefix)

# Loop through each IP in the range 1 to 254
for ($i = 1; $i -le 254; $i++) {
    $IP = "$Prefix.$i"
    try {
        # Perform DNS resolution
        $result = Resolve-DnsName -DnsOnly $IP -Server $Dns -ErrorAction Stop
        Write-Host "Resolved $IP to $($result.IPAddress)"
    }
    catch {
        Write-Host "No response from $IP"
    }
}

