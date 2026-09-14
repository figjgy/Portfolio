# Copy the most recently pasted screenshots out of the Claude uploads folder
# into Portfolio\images\ as marketplace-01.png ... marketplace-NN.png
#
# WHY "most recent" and not a filename: pasted screenshots land as
# <uuid>-<epoch>_image.png — 272 of them and counting. There is nothing in the
# name to match on, so recency is the only handle. That makes this script
# FRAGILE BY NATURE, which is why it prints the timestamp and pixel size of
# every file it takes: a wrong pick is meant to be obvious before the push,
# not after it is live.
#
# Run it BEFORE pasting anything else into the chat.

param([int]$Count = 5, [string]$Prefix = 'marketplace-')

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$imgs = Join-Path $root 'images'
$uploads = 'C:\Users\User\AppData\Roaming\Claude\local-agent-mode-sessions\8b5ba073-8bc7-446f-bf18-2d18fea80703\d91585e8-7aae-42d5-b5b5-88a2eb67b376\local_6c981287-e459-4bb1-9b80-cd3ea9aff432\uploads'

Write-Output "=== SHOP FRONT IMPORT ==="
Write-Output ("date   : " + (Get-Date))
Write-Output ("taking : the $Count most recent images in uploads")
Write-Output ("prefix : $Prefix")
Write-Output ""

if (-not (Test-Path $imgs)) { New-Item -ItemType Directory -Path $imgs | Out-Null }

$files = Get-ChildItem -Path $uploads -File |
         Where-Object { @('.png','.jpg','.jpeg') -contains $_.Extension.ToLower() } |
         Sort-Object LastWriteTime -Descending |
         Select-Object -First $Count

if (-not $files) { Write-Output 'NO IMAGES FOUND in uploads.'; exit 1 }

# Oldest-first so the numbering matches the order they were pasted, which is
# the order she sent them in — left to right on the page.
$files = $files | Sort-Object LastWriteTime

Add-Type -AssemblyName System.Drawing
$i = 0
Write-Output "--- TAKING (check these are the right ones) ---"
foreach ($f in $files) {
  $i++
  $n   = '{0:d2}' -f $i
  $ext = $f.Extension.ToLower(); if ($ext -eq '.jpeg') { $ext = '.jpg' }
  $new = "$Prefix$n$ext"
  $dim = ''
  try {
    $im = [System.Drawing.Image]::FromFile($f.FullName)
    $dim = "  " + $im.Width + "x" + $im.Height
    $im.Dispose()
  } catch { }
  Copy-Item $f.FullName (Join-Path $imgs $new) -Force
  Write-Output ("  " + $f.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss') + "   -> " + $new + $dim)
}

Write-Output ""
Write-Output "--- NOW IN images\ ---"
Get-ChildItem -Path $imgs -Filter "$Prefix*" | ForEach-Object {
  Write-Output ("  " + $_.Name + "   " + [math]::Round($_.Length/1KB) + " KB")
}
Write-Output ""
Write-Output "If any of those timestamps are NOT your shop-front screenshots,"
Write-Output "say so before pushing - nothing else has changed yet."
