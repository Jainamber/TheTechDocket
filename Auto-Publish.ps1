$ErrorActionPreference = "Continue"
$RepoDir = "C:\NewStartsNov\TheTechDocket"
Set-Location $RepoDir

$VenvPy = Join-Path $RepoDir ".venv\Scripts\python.exe"
if (Test-Path $VenvPy) {
    $Python = $VenvPy
} else {
    $Python = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $Python) { $Python = "python" }
}

$Today = Get-Date -Format "yyyy-MM-dd"
$LogFile = Join-Path $RepoDir "data\auto-publish.log"

function Write-Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Out-File -FilePath $LogFile -Append -Encoding utf8
}

function Invoke-Logged([string]$Exe, [string[]]$ArgsList) {
    $out = & $Exe @ArgsList 2>&1
    $code = $LASTEXITCODE
    if ($out) {
        ($out | ForEach-Object { "$_" }) | Out-File -FilePath $LogFile -Append -Encoding utf8
    }
    return $code
}

Write-Log "=== Auto-Publish check for $Today (Python: $Python) ==="

# 1. Pull latest remote changes safely (autostash prevents dirty-tree aborts)
$pullCode = Invoke-Logged "git" @("pull", "--rebase", "--autostash", "origin", "main")
Write-Log "git pull exit=$pullCode"

# 2. Find today's article markdown
$ArticleFile = Get-ChildItem -Path (Join-Path $RepoDir "content\articles") -Filter "$Today-*.md" | Select-Object -First 1
$HistoryPath = Join-Path $RepoDir "data\history.json"
$HistoryText = if (Test-Path $HistoryPath) { Get-Content $HistoryPath -Raw } else { "" }

if ($ArticleFile) {
    $Slug = $ArticleFile.BaseName -replace "^$Today-", ""
    if ($HistoryText -notmatch [regex]::Escape($Slug)) {
        Write-Log "Running live citation_gate for: $Slug"
        $cgCode = Invoke-Logged $Python @("-m", "engine.ai.citation_gate", $Slug)
        if ($cgCode -ne 0) {
            Write-Log "BLOCKED: citation_gate failed for '$Slug' (exit=$cgCode). Skipping article publish."
        } else {
            Write-Log "citation_gate PASSED. Building & publishing article: $Slug"
            $bCode = Invoke-Logged $Python @("-m", "engine.run", "build")
            $gCode = Invoke-Logged $Python @("-m", "engine.run", "gate", "--slug", $Slug)
            if ($gCode -eq 0) {
                $pCode = Invoke-Logged $Python @("-m", "engine.run", "publish", "--slug", $Slug)
                Write-Log "Article publish finished (build=$bCode, gate=$gCode, publish=$pCode)"
            } else {
                Write-Log "BLOCKED: gate failed for '$Slug' (exit=$gCode)."
            }
        }
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
        $null = Invoke-Logged $Python @("-m", "engine.run", "build")
    }
    Write-Log "Publishing docket for $Today"
    $dCode = Invoke-Logged $Python @("-m", "engine.run", "docket-publish", "--date", $Today)
    Write-Log "Docket publish finished (exit=$dCode)"
} else {
    Write-Log "No docket file found for $Today yet."
}

# 4. Ensure any new commits are pushed to origin/main
$pushCode = Invoke-Logged "git" @("push", "origin", "main")
Write-Log "git push exit=$pushCode"
