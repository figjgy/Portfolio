# Extract an uploaded pubmat zip into Portfolio\images\ with predictable names.
#
# Why rename: content.py has to name each file, and the originals arrive with
# spaces, parentheses and mixed case — all of which have to be URL-escaped in an
# <img src> and are easy to get subtly wrong. Sequential ASCII names remove that
# whole class of problem, and the mapping is printed so nothing is lost.
#
# Safe to re-run: it writes into a clean temp folder and never deletes anything
# already in images\ that it did not create.

$ErrorActionPreference = 'Stop'
$root  = Split-Path -Parent $MyInvocation.MyCommand.Path
$imgs  = Join-Path $root 'images'
$tmp   = Join-Path $env:TEMP 'kpick_pubmat_extract'

$uploads = 'C:\Users\User\AppData\Roaming\Claude\local-agent-mode-sessions\8b5ba073-8bc7-446f-bf18-2d18fea80703\d91585e8-7aae-42d5-b5b5-88a2eb67b376\local_6c981287-e459-4bb1-9b80-cd3ea9aff432\uploads'

Write-Output "=== PUBMAT IMPORT ==="
Write-Output ("date        : " + (Get-Date))
Write-Output ("images dir  : " + $imgs)
Write-Output ""

if (-not (Test-Path $imgs)) { New-Item -ItemType Directory -Path $imgs | Out-Null }

# 🔴 NAME THE ZIP, never "take the newest".
# The uploads folder holds ten zips, six of them MARGEGOLD jewellery sets. A
# newest-file rule would happily unpack earrings and file them as
# kpick-medical-01.jpg — wrong pictures under the right name is far worse than
# an error, because nothing downstream would flag it. Match on the name instead
# and refuse if it is not there.
$zip = Get-ChildItem -Path $uploads -Filter '*.zip' -ErrorAction SilentlyContinue |
       Where-Object { $_.Name -like '*MEDICAL*' } |
       Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $zip) {
  Write-Output 'NO ZIP MATCHING "*MEDICAL*" FOUND in uploads. Zips present:'
  Get-ChildItem -Path $uploads -Filter '*.zip' -ErrorAction SilentlyContinue |
    ForEach-Object { Write-Output ("  " + $_.Name) }
  Write-Output ''
  Write-Output 'Nothing was copied. Re-upload the pubmat zip, or tell Claude'
  Write-Output 'which of the above is the right one.'
  exit 1
}
Write-Output ("zip         : " + $zip.Name)
Write-Output ("zip size    : " + [math]::Round($zip.Length/1MB,2) + " MB")
Write-Output ""

if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
New-Item -ItemType Directory -Path $tmp | Out-Null
Expand-Archive -Path $zip.FullName -DestinationPath $tmp -Force

$ok = @('.jpg','.jpeg','.png','.webp')
$files = Get-ChildItem -Path $tmp -Recurse -File |
         Where-Object { $ok -contains $_.Extension.ToLower() } |
         Sort-Object Name

Write-Output ("images found: " + $files.Count)
Write-Output ""
Write-Output "--- MAPPING (original -> new) ---"

$i = 0
foreach ($f in $files) {
  $i++
  $n   = '{0:d2}' -f $i
  $ext = $f.Extension.ToLower()
  if ($ext -eq '.jpeg') { $ext = '.jpg' }
  $new = "kpick-medical-$n$ext"
  Copy-Item $f.FullName (Join-Path $imgs $new) -Force
  $dim = ''
  try {
    Add-Type -AssemblyName System.Drawing
    $im = [System.Drawing.Image]::FromFile($f.FullName)
    $dim = "  [" + $im.Width + "x" + $im.Height + "]"
    $im.Dispose()
  } catch { }
  Write-Output ("  " + $f.Name + "   ->   " + $new + $dim)
}

Write-Output ""
Write-Output "--- FILES NOW IN images\ MATCHING kpick-medical-* ---"
Get-ChildItem -Path $imgs -Filter 'kpick-medical-*' | ForEach-Object {
  Write-Output ("  " + $_.Name + "   " + [math]::Round($_.Length/1KB) + " KB")
}

Remove-Item $tmp -Recurse -Force
Write-Output ""
Write-Output "DONE. Tell Claude the count and it will wire them into content.py."
