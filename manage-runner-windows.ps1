# Palmer AI Runner Management Script for Windows

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "status", "logs")]
    [string]$Action
)

$runnerPath = "$env:USERPROFILE\actions-runner"
$serviceName = "actions.runner.Cbarr32-palmer-ai.palmer-ai-runner-win"

switch ($Action) {
    "start" {
        Write-Host "Starting Palmer AI runner..." -ForegroundColor Green
        Start-Service $serviceName -ErrorAction SilentlyContinue
        if ($?) {
            Write-Host "✅ Runner service started" -ForegroundColor Green
        } else {
            Write-Host "Starting runner in console mode..." -ForegroundColor Yellow
            Set-Location $runnerPath
            Start-Process -FilePath ".\run.cmd" -NoNewWindow
        }
    }
    "stop" {
        Write-Host "Stopping Palmer AI runner..." -ForegroundColor Yellow
        Stop-Service $serviceName -ErrorAction SilentlyContinue
        Get-Process "Runner.Listener", "Runner.Worker" -ErrorAction SilentlyContinue | Stop-Process -Force
        Write-Host "✅ Runner stopped" -ForegroundColor Green
    }
    "status" {
        Write-Host "Palmer AI Runner Status" -ForegroundColor Cyan
        Write-Host "======================" -ForegroundColor Cyan
        
        $service = Get-Service $serviceName -ErrorAction SilentlyContinue
        if ($service) {
            Write-Host "Service Status: $($service.Status)" -ForegroundColor Green
        } else {
            Write-Host "Service Status: Not installed" -ForegroundColor Yellow
        }
        
        $listener = Get-Process "Runner.Listener" -ErrorAction SilentlyContinue
        if ($listener) {
            Write-Host "Listener Process: Running (PID: $($listener.Id))" -ForegroundColor Green
        } else {
            Write-Host "Listener Process: Not running" -ForegroundColor Red
        }
    }
    "logs" {
        Write-Host "Palmer AI Runner Logs" -ForegroundColor Cyan
        Write-Host "===================" -ForegroundColor Cyan
        Set-Location $runnerPath
        Get-Content "_diag\*.log" -Tail 50 | Select-Object -Last 50
    }
}
