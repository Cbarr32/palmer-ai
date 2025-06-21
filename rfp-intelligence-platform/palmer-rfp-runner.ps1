# RFP Intelligence Platform - Complete Task Runner
# Run with: powershell -ExecutionPolicy Bypass -File palmer-rfp-runner.ps1

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "RFP Intelligence Platform Runner"

# Colors
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Clear-Host
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "     RFP Intelligence Platform Task Runner      " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

function Show-Menu {
    Write-Host "SETUP & INSTALLATION" -ForegroundColor Yellow
    Write-Host "  1. Full Setup (Install + Database + Seed)" -ForegroundColor White
    Write-Host "  2. Install Dependencies Only" -ForegroundColor White
    Write-Host "  3. Setup Database (Prisma)" -ForegroundColor White
    Write-Host ""
    Write-Host "DEVELOPMENT" -ForegroundColor Yellow
    Write-Host "  4. Start Development Server" -ForegroundColor White
    Write-Host "  5. Start Dev + Database Studio" -ForegroundColor White
    Write-Host "  6. Open Prisma Studio Only" -ForegroundColor White
    Write-Host ""
    Write-Host "TESTING & QUALITY" -ForegroundColor Yellow
    Write-Host "  7. Run Tests" -ForegroundColor White
    Write-Host "  8. Run Linting" -ForegroundColor White
    Write-Host "  9. Format Code" -ForegroundColor White
    Write-Host ""
    Write-Host "BUILD & DEPLOY" -ForegroundColor Yellow
    Write-Host " 10. Build for Production" -ForegroundColor White
    Write-Host " 11. Analyze Bundle Size" -ForegroundColor White
    Write-Host ""
    Write-Host "UTILITIES" -ForegroundColor Yellow
    Write-Host " 12. Clean Project (Remove Generated Files)" -ForegroundColor White
    Write-Host " 13. Reset Database" -ForegroundColor White
    Write-Host " 14. Check Project Health" -ForegroundColor White
    Write-Host " 15. Update Dependencies" -ForegroundColor White
    Write-Host ""
    Write-Host " 16. Exit" -ForegroundColor Red
    Write-Host ""
}

function Run-FullSetup {
    Write-Host "Running Full Setup..." -ForegroundColor Green
    Write-Host "=====================" -ForegroundColor Green
    
    # Install dependencies
    Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
    npm install --legacy-peer-deps
    
    # Generate Prisma client
    Write-Host "`nGenerating Prisma client..." -ForegroundColor Yellow
    npx prisma generate
    
    # Create .env.local if it doesn't exist
    if (!(Test-Path ".env.local")) {
        Write-Host "`nCreating .env.local file..." -ForegroundColor Yellow
        @"
# AI Provider Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/rfp_platform
DIRECT_URL=postgresql://postgres:password@localhost:5432/rfp_platform

# NextAuth
NEXTAUTH_SECRET=your_secret_here
NEXTAUTH_URL=http://localhost:3000
"@ | Out-File -FilePath ".env.local" -Encoding UTF8
        Write-Host ".env.local created! Please update with your actual keys." -ForegroundColor Green
    }
    
    Write-Host "`nSetup complete!" -ForegroundColor Green
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Update .env.local with your API keys" -ForegroundColor White
    Write-Host "2. Ensure PostgreSQL is running" -ForegroundColor White
    Write-Host "3. Run option 3 to setup database" -ForegroundColor White
    Write-Host "4. Run option 4 to start development" -ForegroundColor White
}

function Check-ProjectHealth {
    Write-Host "Checking Project Health..." -ForegroundColor Green
    Write-Host "=========================" -ForegroundColor Green
    
    $checks = @(
        @{Name="package.json"; Path="package.json"},
        @{Name="node_modules"; Path="node_modules"},
        @{Name="Next.js config"; Path="next.config.js"},
        @{Name="TypeScript config"; Path="tsconfig.json"},
        @{Name="Tailwind config"; Path="tailwind.config.ts"},
        @{Name="Prisma schema"; Path="prisma/schema.prisma"},
        @{Name="App directory"; Path="app"},
        @{Name="Environment file"; Path=".env.local"}
    )
    
    $healthy = $true
    foreach ($check in $checks) {
        if (Test-Path $check.Path) {
            Write-Host "✓ $($check.Name)" -ForegroundColor Green
        } else {
            Write-Host "✗ $($check.Name) - Missing!" -ForegroundColor Red
            $healthy = $false
        }
    }
    
    if ($healthy) {
        Write-Host "`nProject is healthy!" -ForegroundColor Green
    } else {
        Write-Host "`nProject has issues. Run option 1 for full setup." -ForegroundColor Yellow
    }
}

do {
    Show-Menu
    $choice = Read-Host "Select an option (1-16)"
    
    switch ($choice) {
        1 { Run-FullSetup }
        2 { 
            Write-Host "Installing dependencies..." -ForegroundColor Green
            npm install --legacy-peer-deps
        }
        3 {
            Write-Host "Setting up database..." -ForegroundColor Green
            npx prisma generate
            npx prisma migrate dev
        }
        4 {
            Write-Host "Starting development server..." -ForegroundColor Green
            Write-Host "Open http://localhost:3000 in your browser" -ForegroundColor Yellow
            npm run dev
        }
        5 {
            Write-Host "Starting dev server + Prisma Studio..." -ForegroundColor Green
            npm run dev:all
        }
        6 {
            Write-Host "Opening Prisma Studio..." -ForegroundColor Green
            npm run db:studio
        }
        7 {
            Write-Host "Running tests..." -ForegroundColor Green
            npm run test
        }
        8 {
            Write-Host "Running linter..." -ForegroundColor Green
            npm run lint
        }
        9 {
            Write-Host "Formatting code..." -ForegroundColor Green
            npm run format
        }
        10 {
            Write-Host "Building for production..." -ForegroundColor Green
            npm run build
        }
        11 {
            Write-Host "Analyzing bundle..." -ForegroundColor Green
            npm run analyze
        }
        12 {
            Write-Host "Cleaning project..." -ForegroundColor Green
            npm run clean
        }
        13 {
            Write-Host "Resetting database..." -ForegroundColor Yellow
            Write-Host "This will delete all data! Press Ctrl+C to cancel." -ForegroundColor Red
            Start-Sleep -Seconds 3
            npm run db:reset
        }
        14 { Check-ProjectHealth }
        15 {
            Write-Host "Updating dependencies..." -ForegroundColor Green
            npm update
            npm audit fix
        }
        16 {
            Write-Host "Goodbye!" -ForegroundColor Cyan
            exit
        }
        default {
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
        }
    }
    
    if ($choice -ne 16) {
        Write-Host "`nPress Enter to continue..." -ForegroundColor Gray
        Read-Host
        Clear-Host
        Write-Host "================================================" -ForegroundColor Cyan
        Write-Host "     RFP Intelligence Platform Task Runner      " -ForegroundColor Cyan
        Write-Host "================================================" -ForegroundColor Cyan
        Write-Host ""
    }
    
} while ($choice -ne 16)
