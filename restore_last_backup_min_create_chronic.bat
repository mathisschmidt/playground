@echo off
setlocal enabledelayedexpansion
color 0A
title Minecraft Backup Restore Utility

:: Configuration
set "BACKUP_DIR=E:\minecraft\Instances\Create Chronicles The Endventure\simplebackups\New World"
set "SAVE=E:\minecraft\Instances\Create Chronicles The Endventure\saves\New World"

echo ====================================================
echo       MINECRAFT BACKUP RESTORE UTILITY
echo ====================================================
echo.

:: Check if backup directory exists
if not exist "%BACKUP_DIR%" (
    echo [ERROR] Backup directory not found!
    echo Expected location: %BACKUP_DIR%
    echo.
    echo Please check if the path is correct and the drive is accessible.
    pause
    exit /b 1
)

echo [INFO] Backup directory found: %BACKUP_DIR%

:: Look for zip files in backup directory and find the newest one
echo [INFO] Searching for backup zip files...
set "newest_zip="
set "newest_name="
set "newest_date=0"

for %%f in ("%BACKUP_DIR%\*.zip") do (
    for %%a in ("%%f") do (
        set "file_date=%%~ta"
        set "file_date=!file_date: =!"
        set "file_date=!file_date:/=!"
        set "file_date=!file_date::=!"
        
        if !file_date! gtr !newest_date! (
            set "newest_date=!file_date!"
            set "newest_zip=%%f"
            set "newest_name=%%~nxf"
        )
    )
)

if "!newest_zip!"=="" (
    echo [ERROR] No zip backup files found in the backup directory!
    echo Location checked: %BACKUP_DIR%
    echo.
    echo Please ensure your backup zip files are in this location.
    pause
    exit /b 1
)

set "selected_zip=!newest_zip!"
set "selected_name=!newest_name!"

echo.
echo [SUCCESS] Selected backup: !selected_name!

:: Check if SAVE directory exists
if not exist "%SAVE%" (
    echo [ERROR] SAVE directory not found at: %SAVE%
    echo.
    echo Please make sure Minecraft is installed and has been run at least once.
    pause
    exit /b 1
)

echo [SUCCESS] SAVE directory found: %SAVE%

:: Final confirmation
echo.
echo ====================================================
echo                 FINAL CONFIRMATION
echo ====================================================
echo This will completely replace your current Minecraft data with the backup.
echo.
echo Current Minecraft directory: %SAVE%
echo Selected backup file: !selected_name!
echo.
echo WARNING: This action cannot be undone
echo.
set /p "confirm=Are you absolutely sure? Type 'YES' to continue: "

if /i not "!confirm!"=="YES" (
    echo [INFO] Restore cancelled by user.
    pause
    exit /b 0
)

:: Perform the restore
echo.
echo [INFO] Starting restore process...

:: Remove current Minecraft directory
echo [INFO] Removing current Save directory...
rd /s /q "%SAVE%" 2>nul

if exist "%SAVE%" (
    echo [ERROR] Could not remove current SAVE directory!
    echo Please make sure Minecraft is completely closed and try again.
    pause
    exit /b 1
)

:: Extract backup using PowerShell
echo [INFO] Extracting backup...
powershell -Command "Expand-Archive -Path '!selected_zip!' -DestinationPath '%SAVE%' -Force" >nul 2>&1
echo [INFO] copy "%SAVE%\New World" to "%SAVE%".
xcopy "%SAVE%\New World" "%SAVE%" /E /I /H /Y >nul 2>&1

:: Verify extraction
if exist "%SAVE%" (
    echo [SUCCESS] Backup extracted successfully!
) else (
    echo [ERROR] Extraction failed or SAVE directory not found after extraction!
    echo.
    echo This might happen if the backup structure is different than expected.
    echo Please check the backup file contents manually.
    pause
    exit /b 1
)

:: Final verification
echo.
echo ====================================================
echo             RESTORE COMPLETED SUCCESSFULLY!
echo ====================================================
echo.
echo Restore Summary:
echo   * Backup used: !selected_name!
echo   * Restored to: %SAVE%
echo.
echo [SUCCESS] Your Minecraft has been restored from the backup!
echo You can now start Minecraft and your world should be available.
echo.


echo.
echo Press any key to exit...
pause >nul