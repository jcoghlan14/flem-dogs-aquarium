$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$out = Join-Path $root "dist/Flem-Dogs-Aquarium-Windows"
New-Item -ItemType Directory -Force $out | Out-Null
Copy-Item "target/release/aquarium.exe" "$out/Flem-Dogs-Aquarium.exe"
Copy-Item "assets" "$out/assets" -Recurse -Force
Copy-Item "LICENSE-MIT", "LICENSE-APACHE", "WINDOWS-START-HERE.txt" $out
foreach ($entry in @(@("Start Aquarium.cmd", "--windowed"), @("Start Full Screen.cmd", ""), @("Start Low Power.cmd", "--windowed --low-power --quality low"))) {
    $body = "@echo off`r`ncd /d `"%~dp0`"`r`n`"%~dp0Flem-Dogs-Aquarium.exe`" " + $entry[1] + " >> aquarium.log 2>&1`r`nif errorlevel 1 (`r`n echo Aquarium could not start. See aquarium.log.`r`n pause`r`n)`r`n"
    [IO.File]::WriteAllText((Join-Path $out $entry[0]), $body, [Text.Encoding]::ASCII)
}
Compress-Archive -Path $out -DestinationPath "dist/Flem-Dogs-Aquarium-Windows.zip" -Force
