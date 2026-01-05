# GitHub Setup Instructions

## Prerequisites
1. Install Git if not already installed:
   - Download from: https://git-scm.com/download/win
   - Or use: `winget install Git.Git`

## Steps to Push to GitHub

### 1. Initialize Git Repository (if not already done)
```bash
git init
```

### 2. Add All Files
```bash
git add .
```

### 3. Create Initial Commit
```bash
git commit -m "Initial commit: BDD Cucumber Playwright MCP framework for Google search automation"
```

### 4. Create GitHub Repository
- Go to https://github.com/new
- Create a new repository (e.g., `bdd-cucumber-playwright-mcp`)
- **DO NOT** initialize with README, .gitignore, or license (we already have these)

### 5. Add Remote and Push
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Alternative: Using GitHub CLI (if installed)
```bash
gh repo create bdd-cucumber-playwright-mcp --public --source=. --remote=origin --push
```

## Repository Structure
```
.
├── features/
│   ├── google_search.feature
│   ├── steps/
│   │   └── google_search_steps.py
│   └── support/
│       ├── hooks.py
│       ├── mcp_client.py
│       └── world.py
├── pages/
│   └── google_search_page.py
├── reports/
│   └── test_report.html
├── .gitignore
├── behave.ini
├── requirements.txt
└── README.md
```

## What Gets Pushed
- ✅ All source code
- ✅ Feature files
- ✅ Configuration files
- ✅ HTML test reports
- ❌ Python cache files (__pycache__)
- ❌ Virtual environments
- ❌ Log files
- ❌ Screenshots (unless needed)

