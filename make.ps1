# used CHATGPT to generate this script

param(
    [Parameter(Position=0)]
    [string]$Target = "help"
)

function Show-Help {
    Write-Host "Available targets:" -ForegroundColor Green
    Write-Host "  run   - Start the development server"
    Write-Host "  test  - Run all tests"
    Write-Host "  test-conc  - Run concurrency test"
    Write-Host "  help  - Show this help message"
    Write-Host ""
    Write-Host "Usage: .\make.ps1 <target>"
    Write-Host "Example: .\make.ps1 run"
}

function Start-Server {
    Write-Host "Starting development server..." -ForegroundColor Cyan
    uvicorn app.main:app --reload
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Cyan
    pytest tests/
}

function Run-ConcurrencyTest {
    Write-Host "Running concurrency test..." -ForegroundColor Cyan
    python concurrency_test.py
}

switch ($Target.ToLower()) {
    "run" { Start-Server }
    "test" { Run-Tests }
    "test-conc" { Run-ConcurrencyTest }
    "help" { Show-Help }
    default {
        Write-Host "Unknown target: $Target" -ForegroundColor Red
        Write-Host ""
        Show-Help
        exit 1
    }
}
