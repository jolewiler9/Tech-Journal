# dns-resolver.ps1

param($Dns, $Prefix)

# Range of possible IP addresses (assuming /24 subnet)
$Range = 1..254

# Loop through each possible IP in the given network prefix
foreach ($i in $Range) {
    $IP = "$Prefix.$i"
    try {
        # Perform DNS resolution
        $result = Resolve-DnsName -DnsOnly $IP -Server $Dns -ErrorAction Stop
        if ($result) {
            Write-Host "Resolved $IP to $($result.NameHost)"
        }
    }
    catch {
        
    }
}
