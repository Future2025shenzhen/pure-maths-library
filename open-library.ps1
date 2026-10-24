param([string]$Destination = '', [switch]$SkipDownload)
$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($Destination)) {
  $desktop = [Environment]::GetFolderPath('Desktop')
  if ([string]::IsNullOrWhiteSpace($desktop)) { throw 'Cannot find Desktop.' }
  $Destination = Join-Path $desktop 'Cambridge-IGCSE-2019-2024'
}
New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$Destination = (Resolve-Path -LiteralPath $Destination).Path
$kit = $PSScriptRoot
$manifest = Get-Content -LiteralPath (Join-Path $kit 'manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$available = @()
foreach ($item in $manifest.files) {
  $path = Join-Path $Destination $item.relative_path.Replace('/', [IO.Path]::DirectorySeparatorChar)
  if ((Test-Path -LiteralPath $path -PathType Leaf) -and ((Get-Item -LiteralPath $path).Length -eq $item.bytes)) { $available += $item.relative_path }
}
if (($available.Count -eq 0) -and (-not $SkipDownload)) {
  Write-Host 'No downloaded papers found in the desktop folder. Starting the download.'
  & (Join-Path $kit 'download.ps1') -Destination $Destination
  return
}
foreach ($name in @('index.html','manifest.json','file-list.csv','collection-status.json','README.txt')) {
  $from = Join-Path $kit $name; $to = Join-Path $Destination $name
  if ([IO.Path]::GetFullPath($from) -ne [IO.Path]::GetFullPath($to)) { Copy-Item -LiteralPath $from -Destination $to -Force }
}
$availability = ConvertTo-Json -InputObject @($available) -Compress
$js = 'window.PAPER_AVAILABILITY = ' + $availability + ';'
[IO.File]::WriteAllText((Join-Path $Destination 'available.js'), $js, (New-Object Text.UTF8Encoding($false)))
$indexPath = Join-Path $Destination 'index.html'
$uri = ([Uri]$indexPath).AbsoluteUri
Write-Host ('Opening local papers: ' + $available.Count + ' files found.')
$edge = Get-Command 'msedge.exe' -ErrorAction SilentlyContinue
if (-not $edge) {
  foreach ($base in @(${env:ProgramFiles(x86)},$env:ProgramFiles,$env:LOCALAPPDATA)) {
    if (-not [string]::IsNullOrWhiteSpace($base)) {
      $candidate = Join-Path $base 'Microsoft\Edge\Application\msedge.exe'
      if (Test-Path -LiteralPath $candidate) { $edge = [PSCustomObject]@{ Source=$candidate }; break }
    }
  }
}
if ($edge) { Start-Process -FilePath $edge.Source -ArgumentList ('"' + $uri + '"') }
else { Start-Process -FilePath $indexPath }
