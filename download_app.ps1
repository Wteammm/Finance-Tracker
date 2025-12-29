# PowerShell script to download app.py from PythonAnywhere
# This will attempt to download the file using Invoke-WebRequest

$url = "https://www.pythonanywhere.com/user/wtea/files/home/wtea/Finance_Tracker/app.py?download"
$outputFile = "app_from_pa.py"

try {
    # Try to download without authentication (might work if browser session exists)
    Invoke-WebRequest -Uri $url -OutFile $outputFile -UseBasicParsing
    
    $fileInfo = Get-Item $outputFile
    Write-Host "Success! Downloaded file:"
    Write-Host "  Size: $($fileInfo.Length) bytes"
    Write-Host "  Lines: $((Get-Content $outputFile | Measure-Object -Line).Lines)"
} catch {
    Write-Host "Error: $_"
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)"
}
