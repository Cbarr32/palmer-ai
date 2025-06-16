# Palmer AI Runner Control Center
param(
    [string]$Action = "status"
)

# Find the service
$serviceName = Get-Service -Name "actions.runner.*palmer*" -ErrorAction SilentlyContinue | Select -First 1 -ExpandProperty Name

if (-not $serviceName) {
    Write-Host "❌ No Palmer AI runner service found!" -ForegroundColor Red
    Write-Host "The runner may be running in console mode." -ForegroundColor Yellow
    
    # Check for console runner
    $runnerProcess = Get-Process "Runner.Listener" -ErrorAction SilentlyContinue
    if ($runnerProcess) {
        Write-Host "✅ Found runner in console mode (PID: $($runnerProcess.Id))" -ForegroundColor Green
    }
    exit
}

switch ($Action.ToLower()) {
    "status" {
        $service = Get-Service $serviceName
        Write-Host "`nPalmer AI Runner Status" -ForegroundColor Cyan
        Write-Host "======================" -ForegroundColor Cyan
        Write-Host "Service: $serviceName"
        Write-Host "Status: $($service.Status)" -ForegroundColor $(if($service.Status -eq 'Running'){'Green'}else{'Red'})
        Write-Host "Startup: $($service.StartType)"
        
        # Check GitHub connectivity
        if ($service.Status -eq 'Running') {
            Write-Host "`n✅ Runner service is operational" -ForegroundColor Green
            Write-Host "Check GitHub Actions at: https://github.com/Cbarr32/palmer-ai/settings/actions/runners"
        }
    }
    "start" {
        Start-Service $serviceName
        Write-Host "✅ Starting runner service..." -ForegroundColor Green
    }
    "stop" {
        Stop-Service $serviceName -Force
        Write-Host "✅ Stopping runner service..." -ForegroundColor Yellow
    }
    "restart" {
        Restart-Service $serviceName -Force
        Write-Host "✅ Restarting runner service..." -ForegroundColor Green
    }
    "logs" {
        $runnerPath = (Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\$serviceName" -Name ImagePath -ErrorAction SilentlyContinue).ImagePath
        if ($runnerPath) {
            $logPath = Split-Path $runnerPath | Join-Path -ChildPath "_diag"
            Get-ChildItem "$logPath\*.log" | Sort LastWriteTime -Descending | Select -First 1 | Get-Content -Tail 50
        }
    }
}
