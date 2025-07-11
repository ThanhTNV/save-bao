# Start Python service with uvicorn
$pythonProcess = Start-Process -FilePath "uvicorn" -ArgumentList "main:app --host 0.0.0.0 --port 8000" -WorkingDirectory ".\pthon" -PassThru -WindowStyle Normal

# Start ASP.NET Core service
$dotnetProcess = Start-Process -FilePath "dotnet" -ArgumentList "run --project .\WebApi" -PassThru -WindowStyle Normal

Write-Host "Both services are running..."
Write-Host "Python service running on http://localhost:8000"
Write-Host "Press Ctrl+C to stop all services"

try {
    Wait-Process -Id $pythonProcess.Id, $dotnetProcess.Id -ErrorAction SilentlyContinue
} finally {
    # Cleanup when script is interrupted
    if (!$pythonProcess.HasExited) { Stop-Process -Id $pythonProcess.Id -Force }
    if (!$dotnetProcess.HasExited) { Stop-Process -Id $dotnetProcess.Id -Force }
    Write-Host "`nServices stopped."
} 