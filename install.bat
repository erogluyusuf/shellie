@echo off
setlocal
title Shellie Kurulum Sihirbazi
echo [Shellie] Sistem gereksinimleri ve kutuphaneler kontrol ediliyor...
echo ---------------------------------------------------

:: ========================================================
:: 1. VISUAL C++ REDISTRIBUTABLE KONTROLU (YENI)
:: ========================================================
echo [Shellie] Visual C++ Kutuphaneleri kontrol ediliyor...

:: Basit bir kontrol: VC++ gerektiren bir komut dene
reg query "HKLM\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" /v Installed >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Visual C++ Redistributable zaten yuklu.
    goto :CHECK_PYTHON
)

echo [!] Visual C++ eksik. PHP icin bu gerekli.
echo [!] Otomatik olarak indiriliyor ve kuruluyor...

:: Winget ile sessizce kur
winget install --id Microsoft.VCRedist.2015+.x64 -e --accept-package-agreements --accept-source-agreements

if %errorlevel% neq 0 (
    echo [UYARI] Winget ile kurulamadi. Lutfen manuel kurun: https://aka.ms/vs/17/release/vc_redist.x64.exe
    echo Devam ediliyor...
) else (
    echo [OK] Visual C++ basariyla kuruldu.
)

:: ========================================================
:: 2. PYTHON KONTROLU
:: ========================================================
:CHECK_PYTHON
echo.
echo [Shellie] Python kontrol ediliyor...

set PY_CMD=
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PY_CMD=python
    goto :PYTHON_FOUND
)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PY_CMD=py
    goto :PYTHON_FOUND
)

echo [!] Python bulunamadi. Yukleniyor...
winget install -e --id Python.Python.3.12 --scope machine --accept-package-agreements --accept-source-agreements
set PY_CMD=py

:PYTHON_FOUND
echo [OK] Python: %PY_CMD%

:: ========================================================
:: 3. PHP KONTROLU (Artik Portable Kullandigimiz Icin Atliyoruz)
:: ========================================================
:: Biz PHP'yi klasorun icine koyduk, bu yuzden sisteme kurmaya gerek yok.
:: Sadece VC++ (yukaridaki adim) yeterli.

:: ========================================================
:: 4. KUTUPHANE KURULUMU
:: ========================================================
echo.
echo [Shellie] Python paketleri yukleniyor...

if not exist requirements.txt (
    echo PyQt6 > requirements.txt
    echo psutil >> requirements.txt
)

%PY_CMD% -m pip install --upgrade pip
%PY_CMD% -m pip install -r requirements.txt

echo.
echo ---------------------------------------------------
echo [Shellie] KURULUM TAMAMLANDI!
python src/main.py
pause
