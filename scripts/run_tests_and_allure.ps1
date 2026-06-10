$ErrorActionPreference = "Stop"

function Import-DotEnv {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Path
  )
  if (!(Test-Path $Path)) { return }

  Get-Content $Path | ForEach-Object {
    $line = $_.Trim()
    if ($line.Length -eq 0) { return }
    if ($line.StartsWith("#")) { return }
    if (!($line.Contains("="))) { return }

    $idx = $line.IndexOf("=")
    $key = $line.Substring(0, $idx).Trim()
    $val = $line.Substring($idx + 1).Trim()

    # 去掉可选的引号
    if (($val.StartsWith('"') -and $val.EndsWith('"')) -or ($val.StartsWith("'") -and $val.EndsWith("'"))) {
      $val = $val.Substring(1, $val.Length - 2)
    }

    if ($key.Length -gt 0) {
      Set-Item -Path "Env:$key" -Value $val
    }
  }
}

$root = Split-Path -Parent $PSScriptRoot
Import-DotEnv -Path (Join-Path $root ".env")

if (-not $env:ALLURE_RESULTS_DIR) { $env:ALLURE_RESULTS_DIR = "allure-results" }
if (-not $env:ALLURE_PATH) {
  $env:ALLURE_PATH = "F:\allure-commandline-2.35.1\allure-2.35.1\bin\allure.bat"
}

Write-Host "==> 运行 pytest 并输出到 $env:ALLURE_RESULTS_DIR"
python -m pytest -s --alluredir="$env:ALLURE_RESULTS_DIR"

Write-Host "==> 启动 Allure 并自动打开浏览器"
& "$env:ALLURE_PATH" serve "$env:ALLURE_RESULTS_DIR"

