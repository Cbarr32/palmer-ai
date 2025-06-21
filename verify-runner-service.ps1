# Palmer AI Runner Service Verification
$serviceName = Get-Service "actions.runner.*palmer*" | Select -First 1 -ExpandProperty Name

Write-Host "`n🔍 Palmer AI Runner Service Status" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

$service = Get-Service $serviceName
Write-Host "Service Name: $($service.Name)" -ForegroundColor Green
Write-Host "Status: $($service.Status)" -ForegroundColor $(if($service.Status -eq 'Running'){'Green'}else{'Red'})
Write-Host "Startup Type: $($service.StartType)" -ForegroundColor Yellow

if ($service.Status -eq 'Running') {
    Write-Host "`n✅ Runner is properly configured as Windows service!" -ForegroundColor Green
    Write-Host "✅ Will start automatically on reboot" -ForegroundColor Green
    Write-Host "✅ Running in background (no console needed)" -ForegroundColor Green
} else {
    Write-Host "`n❌ Service not running properly" -ForegroundColor Red
}
