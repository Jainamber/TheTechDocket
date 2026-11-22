$ErrorActionPreference = "Stop"
$RepoDir = "C:\NewStartsNov\TheTechDocket"
Set-Location $RepoDir

$Python = Join-Path $RepoDir ".venv\Scripts\python.exe"
$Today = Get-Date -Format "yyyy-MM-dd"
$LogFile = Join-Path $RepoDir "data\auto-publish.log"

function Write-Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Out-File -FilePath $LogFile -Append -Encoding utf8
}

Write-Log "=== Auto-Publish check for $Today ==="

# 1. Pull latest remote changes so push never rejects
git pull --rebase origin main 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8

# 2. Find today's article markdown
$ArticleFile = Get-ChildItem -Path (Join-Path $RepoDir "content\articles") -Filter "$Today-*.md" | Select-Object -First 1
$HistoryPath = Join-Path $RepoDir "data\history.json"
$HistoryText = if (Test-Path $HistoryPath) { Get-Content $HistoryPath -Raw } else { "" }

if ($ArticleFile) {
    $Slug = $ArticleFile.BaseName -replace "^$Today-", ""
    if ($HistoryText -notmatch [regex]::Escape($Slug)) {
        Write-Log "Building & publishing article: $Slug"
        & $Python -m engine.run build 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
        & $Python -m engine.run publish --slug $Slug 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
        Write-Log "Article publish finished (exit=$LASTEXITCODE)"
    } else {
        Write-Log "Article '$Slug' already published in history.json; skipping."
    }
} else {
    Write-Log "No article file found for $Today yet."
}

# 3. Find today's docket markdown
$DocketFile = Join-Path $RepoDir "data\docket\$Today.md"
$DocketHtml = Join-Path $RepoDir "docs\docket\$Today\index.html"
if (Test-Path $DocketFile) {
    if (-not (Test-Path $DocketHtml)) {
        Write-Log "Building site for docket $Today"
        & $Python -m engine.run build 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
    }
    Write-Log "Publishing docket for $Today"
    & $Python -m engine.run docket-publish --date $Today 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
    Write-Log "Docket publish finished (exit=$LASTEXITCODE)"
} else {
    Write-Log "No docket file found for $Today yet."
}
