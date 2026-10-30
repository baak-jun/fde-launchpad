$ErrorActionPreference = 'Stop'
$rootPath = Split-Path -Parent $PSScriptRoot
$previousTemp = $env:TEMP
$previousTmp = $env:TMP
Push-Location $rootPath
try {
    New-Item -ItemType Directory -Force '.cache/wheels','.cache/tmp' | Out-Null
    $env:TEMP = Join-Path $rootPath '.cache/tmp'
    $env:TMP = $env:TEMP
    .venv/Scripts/python.exe -m pip download --cache-dir .cache/pip --only-binary=:all: --dest .cache/wheels -r requirements.lock
    if ($LASTEXITCODE -ne 0) { throw 'Wheel cache incomplete. Inspect platform/version compatibility.' }
    Write-Output 'Wheel cache prepared for this Python/OS/architecture only; it is excluded from source backups.'
} finally {
    $env:TEMP = $previousTemp
    $env:TMP = $previousTmp
    Pop-Location
}
