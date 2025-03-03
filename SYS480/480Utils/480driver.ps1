Import-Module '480-utils' -Force

# Call the Banner Function
480Banner

# Load configuration
$conf = Get-480Config -config_path "/home/jared-adm/Documents/SYS-480/480.json"

# Connect to VCenter
480Connect -server $conf.vcenter_server

# Selecting VM for cloning
Write-Host "Selecting your VM"
$sourceVM = Select-VM
if (-not $sourceVM)
{
    Write-Host "No valid VM selected. Exiting..." -ForegroundColor "Red"
    exit
}

# Get final bit of information for clone from the user
$cloneName = Read-Host "Enter the name for the new linked clone"
$esxiHost = Read-Host "Enter the target ESXi host"
$datastore = Read-Host "Enter the datastore name"

# Create linked clone
New-LinkedClone -sourceVM $sourceVM.Name -cloneName $cloneName -esxiHost $esxiHost -datastore $datastore
