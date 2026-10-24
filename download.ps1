param([string]$Destination = '')
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$kit = $PSScriptRoot
$manifestPath = Join-Path $kit 'manifest.json'
if ([string]::IsNullOrWhiteSpace($Destination)) {
  $desktop = [Environment]::GetFolderPath('Desktop')
  if ([string]::IsNullOrWhiteSpace($desktop)) { throw 'Cannot find Desktop. Run with -Destination C:\your-folder' }
  $Destination = Join-Path $desktop 'Cambridge-IGCSE-2019-2024'
}
New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$Destination = (Resolve-Path -LiteralPath $Destination).Path
foreach ($name in @('manifest.json','file-list.csv','index.html','collection-status.json','README.txt')) {
  Copy-Item -LiteralPath (Join-Path $kit $name) -Destination (Join-Path $Destination $name) -Force
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$total = @($manifest.files).Count
Write-Host ('Target: ' + $Destination)
Write-Host ('Files: ' + $total + '. Internet is required. Existing verified files will be skipped.')
Write-Host 'Keep this window open. You can rerun START-DOWNLOAD.cmd after an interruption.'
$worker = {
  param($manifestPath, $destination, $workerIndex, $workers)
  $ErrorActionPreference = 'Stop'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $items = @((Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json).files)
  for ($i = $workerIndex; $i -lt $items.Count; $i += $workers) {
    $item = $items[$i]
    $relative = $item.relative_path.Replace('/', [IO.Path]::DirectorySeparatorChar)
    $path = Join-Path $destination $relative
    $state = 'failed'; $message = ''
    try {
      New-Item -ItemType Directory -Force -Path (Split-Path -Parent $path) | Out-Null
      if ((Test-Path -LiteralPath $path) -and ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -eq $item.sha256)) {
        $state = 'already verified'
      } else {
        for ($attempt = 1; $attempt -le 3; $attempt++) {
          $temporary = $path + '.part'
          try {
            $url = $item.url
            if ($attempt -eq 2) {
              $url = $url -replace '^https://raw.githubusercontent.com/([^/]+)/([^/]+)/', 'https://github.com/$1/$2/raw/'
            }
            Invoke-WebRequest -Uri $url -UseBasicParsing -OutFile $temporary -TimeoutSec 90 -ErrorAction Stop | Out-Null
            if ((Get-FileHash -LiteralPath $temporary -Algorithm SHA256).Hash -ne $item.sha256) { throw 'SHA-256 does not match the verified original.' }
            Move-Item -LiteralPath $temporary -Destination $path -Force
            $state = 'downloaded'; $message = ''; break
          } catch {
            $message = $_.Exception.Message
            if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary -Force }
          }
        }
      }
    } catch { $message = $_.Exception.Message }
    [PSCustomObject]@{ file=$item.relative_path; status=$state; message=$message }
  }
}
$jobs = @(); $results = New-Object 'System.Collections.Generic.List[object]'
try {
  for ($w=0; $w -lt 4; $w++) { $jobs += Start-Job -ScriptBlock $worker -ArgumentList $manifestPath,$Destination,$w,4 }
  do {
    foreach ($j in $jobs) {
      foreach ($record in @(Receive-Job -Job $j -ErrorAction Continue)) {
        if ($null -ne $record.file) {
          $results.Add($record)
          if ($record.status -eq 'failed') { Write-Host ('FAILED: ' + $record.file) -ForegroundColor Yellow }
        }
      }
    }
    Write-Progress -Activity 'Downloading Cambridge IGCSE papers' -Status ($results.Count.ToString() + ' / ' + $total) -PercentComplete ([Math]::Min(100,100*$results.Count/[Math]::Max(1,$total)))
    $active = @($jobs | Where-Object { $_.State -eq 'Running' -or $_.State -eq 'NotStarted' }).Count
    if ($active -gt 0) { Start-Sleep -Milliseconds 300 }
  } while ($active -gt 0)
  foreach ($j in $jobs) { foreach ($record in @(Receive-Job -Job $j -ErrorAction Continue)) { if ($null -ne $record.file) { $results.Add($record) } } }
} finally {
  foreach ($j in $jobs) { if ($j.State -eq 'Running') { Stop-Job -Job $j }; Remove-Job -Job $j -Force }
  $results | Select-Object file,status,message | Export-Csv -LiteralPath (Join-Path $Destination 'download-log.csv') -NoTypeInformation -Encoding UTF8
  Write-Progress -Activity 'Downloading Cambridge IGCSE papers' -Completed
}
$failed = @($results | Where-Object { $_.status -eq 'failed' }).Count
$verified = @($results | Where-Object { $_.status -ne 'failed' }).Count
Write-Host ('Verified files: ' + $verified + ' / ' + $total)
Write-Host ('Failed files: ' + $failed)
if ($verified -ne $total) { Write-Host 'NOT COMPLETE. Check download-log.csv, then rerun to retry.' -ForegroundColor Yellow }
else { Write-Host 'Download complete. Open index.html in the desktop folder.' -ForegroundColor Green }
& (Join-Path $kit 'open-library.ps1') -Destination $Destination -SkipDownload
