# Step 1: Make the initial request to fetch the href and mfa_validate values
$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/tokens/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C" `
                              -AllowUnencryptedAuth `
                              -Headers @{ "Cookie" = "token=5f8dd236f862f4507835b0e418907ffc" } `
                              -Credential (New-Object System.Management.Automation.PSCredential("admin", (ConvertTo-SecureString "admin" -AsPlainText -Force)))

# Extract href and mfa_validate values from the response

# Extract the href value using a regular expression
# Example content (replace with $response.Content)
$responseContent = $response.Content

# Extract href value
if ($responseContent -match "href='([^']*)'") {
    $hrefValue = $matches[1]
} else {
    $hrefValue = $null
}

# Extract the part after /mfa_validate/
if ($responseContent -match "/mfa_validate/([^<]*)") {
    $mfaValidatePath = $matches[1]
} else {
    $mfaValidatePath = $null
}

# Output the results
#"href: $hrefValue"
#"mfa_validate: $mfaValidatePath"


# Step 2: Use the extracted values in the second request
$response2 = Invoke-WebRequest -Uri "http://127.0.0.1:1225/mfa_validate/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C" `
                               -AllowUnencryptedAuth `
                               -Credential (New-Object System.Management.Automation.PSCredential("admin", (ConvertTo-SecureString "admin" -AsPlainText -Force))) `
                               -Headers @{ "Cookie" = "mfa_token=$hrefValue; token=5f8dd236f862f4507835b0e418907ffc" }

# Output the second response content
$response2.Content
