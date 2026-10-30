param([switch]$Offline, [string]$WheelDirectory = '')
$ErrorActionPreference = 'Stop'
$rootPath = Split-Path -Parent $PSScriptRoot
$previousTemp = $env:TEMP
$previousTmp = $env:TMP
$previousEncoding = $env:PYTHONIOENCODING
Push-Location $rootPath
try {
    New-Item -ItemType Directory -Force '.cache/tmp','.cache/pip' | Out-Null
    $env:TEMP = Join-Path $rootPath '.cache/tmp'
    $env:TMP = $env:TEMP
    $env:PYTHONIOENCODING = 'utf-8'
    if (-not (Test-Path '.venv/Scripts/python.exe')) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
    }
    $pythonPath = Join-Path $rootPath '.venv/Scripts/python.exe'
    & $pythonPath -m ensurepip --upgrade
    if ($LASTEXITCODE -ne 0) { throw 'pip setup failed.' }
    if ($Offline) {
        $wheelPath = if ($WheelDirectory) { $WheelDirectory } else { Join-Path $rootPath '.cache/wheels' }
        if (-not (Test-Path -LiteralPath $wheelPath)) { throw 'No offline wheel cache. Run scripts/cache_wheels.ps1 while online first.' }
        & $pythonPath -m pip install --no-index --find-links $wheelPath -r requirements.lock
    } else {
        & $pythonPath -m pip install --cache-dir .cache/pip -r requirements.lock
    }
    if ($LASTEXITCODE -ne 0) { throw 'Dependency install failed.' }
    & $pythonPath -m pip check
    if ($LASTEXITCODE -ne 0) { throw 'Dependency check failed.' }
    Write-Output 'Ready: .venv/Scripts/python.exe run_workbench.py'
} finally {
    $env:TEMP = $previousTemp
    $env:TMP = $previousTmp
    $env:PYTHONIOENCODING = $previousEncoding
    Pop-Location
}
