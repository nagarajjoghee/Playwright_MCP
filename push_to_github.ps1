# GitHub Push Script
Write-Host "=== Push to GitHub ===" -ForegroundColor Cyan
Write-Host ""

# Get GitHub username
$username = Read-Host "Enter your GitHub username"
if ([string]::IsNullOrWhiteSpace($username)) {
    Write-Host "Username is required!" -ForegroundColor Red
    exit 1
}

# Get repository name
$repoName = Read-Host "Enter your repository name"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    Write-Host "Repository name is required!" -ForegroundColor Red
    exit 1
}

# Construct the remote URL
$remoteUrl = "https://github.com/$username/$repoName.git"

Write-Host ""
Write-Host "Repository URL: $remoteUrl" -ForegroundColor Yellow
Write-Host ""

# Check if remote already exists
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to update it? (y/n)"
    if ($overwrite -eq 'y' -or $overwrite -eq 'Y') {
        git remote set-url origin $remoteUrl
        Write-Host "✓ Remote URL updated" -ForegroundColor Green
    } else {
        Write-Host "Keeping existing remote" -ForegroundColor Yellow
    }
} else {
    Write-Host "Adding remote repository..." -ForegroundColor Yellow
    git remote add origin $remoteUrl
    Write-Host "✓ Remote added" -ForegroundColor Green
}

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host ""

# Push to GitHub
try {
    git push -u origin main
    Write-Host ""
    Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "View your repository at: https://github.com/$username/$repoName" -ForegroundColor Cyan
} catch {
    Write-Host ""
    Write-Host "✗ Error pushing to GitHub" -ForegroundColor Red
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "  1. The repository exists on GitHub" -ForegroundColor White
    Write-Host "  2. You have access to push to it" -ForegroundColor White
    Write-Host "  3. You're authenticated (may need Personal Access Token)" -ForegroundColor White
    Write-Host ""
    Write-Host "If authentication fails, you may need to:" -ForegroundColor Yellow
    Write-Host "  - Use a Personal Access Token instead of password" -ForegroundColor White
    Write-Host "  - Create token at: https://github.com/settings/tokens" -ForegroundColor White
}

