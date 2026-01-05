# Git Setup and Push Script for BDD Cucumber Playwright MCP Project

Write-Host "=== GitHub Setup Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git first:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "  2. Or run: winget install Git.Git" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "Step 1: Initializing Git repository..." -ForegroundColor Yellow

# Initialize git if not already done
if (Test-Path .git) {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
} else {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Adding files to staging..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added to staging" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Checking for existing commits..." -ForegroundColor Yellow
$commitCount = (git rev-list --count HEAD 2>$null)
if ($commitCount -eq 0) {
    Write-Host "Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: BDD Cucumber Playwright MCP framework for Google search automation"
    Write-Host "✓ Initial commit created" -ForegroundColor Green
} else {
    Write-Host "✓ Repository already has commits" -ForegroundColor Green
    Write-Host "Current commits: $commitCount" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Step 4: Checking for remote repository..." -ForegroundColor Yellow
$remote = git remote get-url origin 2>$null
if ($remote) {
    Write-Host "✓ Remote repository found: $remote" -ForegroundColor Green
    Write-Host ""
    Write-Host "To push to GitHub, run:" -ForegroundColor Yellow
    Write-Host "  git push -u origin main" -ForegroundColor White
} else {
    Write-Host "✗ No remote repository configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Create a new repository on GitHub (https://github.com/new)" -ForegroundColor White
    Write-Host "  2. Run the following commands:" -ForegroundColor White
    Write-Host "     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git" -ForegroundColor Cyan
    Write-Host "     git branch -M main" -ForegroundColor Cyan
    Write-Host "     git push -u origin main" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""

