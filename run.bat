@echo off
cd /d "%~dp0"
tasklist /FI "IMAGENAME eq php.exe" | find /I "php.exe" >nul
if errorlevel 1 (
    start /b "" "php\php.exe" -S localhost:8080 -t dashboard
    timeout /t 1 >nul
)
start http://localhost:8080
exit
