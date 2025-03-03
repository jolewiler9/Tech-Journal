# Show SYS480 Banner
Function 480Banner()
{
	Write-Host "Hi There SYS480!"
}

Function Get-480Config([string] $config_path)
{
	Write-Host "Reading " $config_path
	$conf=$null
	if(Test-Path $config_path)
	{
		$conf = (Get-Content -Raw -Path $config_path | ConvertFrom-Json)
		$msg = "Using Configuration at {0}" -f $config_path
		Write-Host -ForegroundColor "Green" $msg
	}else
	{
		Write-Host -ForegroundColor "Yellow" "No Configuration"
	}
	return $conf
}

# Connect to VCenter Server
Function 480Connect([string] $server)
{
	$conn = $global:DefaultVIServer
	if ($conn){
		$msg = "Already Connected to {0}" -f $conn
		
		Write-Host -ForegroundColor Green $msg
	}else
	{
		$conn = Connect-VIServer -Server $server
	}
}

Function Select-VM()
{
	$selected_vm=$null
	try
	{
		$vms = Get-VM
		$index = 1
		foreach($vm in $vms)
		{
			Write-Host [$index] $vm.name
			$index+=1
		}
		$pick_index = Read-Host "Which number do you wish to pick?"
		$selected_vm = $vms[$pick_index -1]
		Write-Host "You picked " $selected_vm.name
		return $selected_vm
}
	catch
	{
		Write-Host "Invalid Folder: $folder" -ForegorundColor "Red"
	}
}

Function New-LinkedClone
{
	param (
		[string]$sourceVM,
		[string]$cloneName,
		[string]$esxiHost,
		[string]$datastore
	)

	try
	{
		# Validate the source VM exists
		$vm = Get-VM -Name $sourceVM -ErrorAction Stop
		if (-not $vm)
		{
			Write-Host "Error: VM '$sourceVM' does not exist" -ForegroundColor "Red"
			return
		}

		# Validate that the VM has a BASE snapshot
		$snapshot = Get-Snapshot -VM $vm | Where-Object { $_.Name -eq "Base" }
		if (-not $snapshot)
		{
			Write-Host "Error: No 'Base' snapshot found for VM selected" -ForegoundColor "Red"
			return
		}

		# Validate that the ESXI host exists
		$vmhost = Get-VMHost -Name $esxiHost -ErrorAction Stop
		if (-not $vmhost)
		{
			Write-Host "Error: ESXi Host does not exist" -ForegroundColor "Red"
			return
		}

		# Validate the datastore exists
		$ds = Get-Datastore -Name $datastore -ErrorAction Stop
		if (-not $ds)
		{
			Write-Host "Error: Datastore '$datastore' does not exist"
			return
		}

		# Create the linked clone
		Write-Host "Creating Linked Clone '$cloneName' from '$sourceVM'..."
		New-VM -Name $cloneName -VM $vm -LinkedClone -ReferenceSnapshot $snapshot -VMHost $vmhost -Datastore $ds

		Write-Host "Linked Clone '$cloneName' created successfully!" -ForegroundColor "Green"
	}
	catch
	{
		Write-Host "Error: $_" -ForegroundColor "Red"
	}
}