@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem ================================================================
rem 1) SCRIPT ROOT AND BASE PATHS
rem ================================================================

rem %~dp0 is the folder where this .bat file lives.
rem Keeping SOURCE_ROOT tied to script location makes the script portable.
set "SOURCE_ROOT=%~dp0"

rem ================================================================
rem 2) DESTINATION FOLDER RESOLUTION
rem ================================================================

rem Destination selection mode:
rem   1 = prefer SPACE_EXPORT_DIR environment variable
rem   0 = ignore SPACE_EXPORT_DIR and use MANUAL_DESTINATION below
set "USE_ENV_DESTINATION=1"

rem Used when USE_ENV_DESTINATION=0.
set "MANUAL_DESTINATION=%~dp0exported_text_files"

rem Tip: persist SPACE_EXPORT_DIR with setx SPACE_EXPORT_DIR "C:\path\to\folder"
if "%USE_ENV_DESTINATION%"=="1" (
    rem First try process-level env var (works in terminals where it is already loaded).
    if not defined SPACE_EXPORT_DIR (
        rem If terminal is older than setx call, read user-level value directly from registry.
        rem `reg query ... /v SPACE_EXPORT_DIR` prints one matching line with type and value.
        rem for /F with "tokens=2,*" captures everything after the type into %%B, including spaces.
        rem `2^>nul` hides "value not found" stderr, and findstr keeps only the named variable line.
        for /F "tokens=2,*" %%A in ('reg query HKCU\Environment /v SPACE_EXPORT_DIR 2^>nul ^| findstr /R /C:"SPACE_EXPORT_DIR"') do set "SPACE_EXPORT_DIR=%%B"
    )

    rem If env var still not available, fallback to local default folder.
    if not defined SPACE_EXPORT_DIR set "SPACE_EXPORT_DIR=%~dp0exported_text_files"
    set "DESTINATION_FOLDER=!SPACE_EXPORT_DIR!"
) else (
    set "DESTINATION_FOLDER=!MANUAL_DESTINATION!"
)

if not exist "%DESTINATION_FOLDER%" mkdir "%DESTINATION_FOLDER%"

rem -----------------------------------------------------------------
rem Mapping section:
rem   FILEn     = source path, relative to SOURCE_ROOT
rem   FILEnCOPY = destination filename in DESTINATION_FOLDER
rem
rem You can skip numbers (for example FILE3 missing) safely.
rem The loop checks each index and only copies when FILEn is defined.
rem -----------------------------------------------------------------
set "FILE1=galaxy\admin.py"
set "FILE1COPY=admin.txt"

set "FILE2=galaxy\models.py"
set "FILE2COPY=models.txt"

set "FILE4=galaxy\urls.py"
set "FILE4COPY=galaxy_app_urls.txt"

set "FILE5=galaxy\views.py"
set "FILE5COPY=views.txt"

set "FILE6=templates\base.html"
set "FILE6COPY=html_base.txt"

set "FILE7=templates\galaxy\body_detail.html"
set "FILE7COPY=html_body_detail.txt"

set "FILE8=templates\galaxy\mining_spot_detail.html"
set "FILE8COPY=html_mining_spot_detail.txt"

set "FILE9=templates\galaxy\system_confirm_delete.html"
set "FILE9COPY=html_system_confirm_delete.txt"

set "FILE10=templates\galaxy\system_detail.html"
set "FILE10COPY=html_system_detail.txt"

set "FILE11=templates\galaxy\system_form.html"
set "FILE11COPY=html_system_form.txt"

set "FILE12=templates\galaxy\system_list.html"
set "FILE12COPY=html_system_list.txt"

set "FILE13=spacenotes\urls.py"
set "FILE13COPY=spacenotes_project_urls.txt"

set "FILE14=spacenotes\settings.py"
set "FILE14COPY=settings.txt"

rem ================================================================
rem 3) LOOP SETTINGS AND VALIDATION RULES
rem ================================================================

rem Highest mapping index to inspect.
set "MAX_INDEX=50"

rem Allowed destination filename extensions (space-separated list).
rem Keep this as .txt only if you always want text files.
set "ALLOWED_EXTENSIONS=.txt"

rem ================================================================
rem 4) MAIN COPY EXECUTION LOOP
rem ================================================================

rem /L means numeric loop: (start,step,end). Here it checks FILE1..FILE%MAX_INDEX%.
rem This avoids hardcoding many call lines and safely tolerates missing indexes.
for /L %%I in (1,1,%MAX_INDEX%) do (
    rem Dynamic variable lookup: !FILE%%I! means FILE1, FILE2, ... at runtime.
    call set "SOURCE_REL=%%FILE%%I%%"
    call set "DEST_NAME=%%FILE%%ICOPY%%"

    rem If FILE%%I is undefined/empty, this index is ignored.
    if defined SOURCE_REL (
        call :copy_file "!SOURCE_REL!" "!DEST_NAME!" %%I
        if errorlevel 1 exit /b 1
    )
)

echo.
echo Done. Copied mapped files to "%DESTINATION_FOLDER%".
exit /b 0

:copy_file
rem ================================================================
rem 5) SUBROUTINE: COPY A SINGLE MAPPING
rem ================================================================

rem %1, %2, %3 are arguments passed to this label from: call :copy_file "src" "dest" index
rem %~1 strips surrounding quotes from argument 1 (same for %~2 and %~3).
rem We quote values again in set commands to safely preserve spaces/special characters.
set "SOURCE_REL=%~1"
set "DEST_NAME=%~2"
set "MAP_INDEX=%~3"

if "%DEST_NAME%"=="" (
    echo Mapping error at FILE%MAP_INDEX%: missing FILE%MAP_INDEX%COPY destination name.
    exit /b 1
)

call :validate_extension "%DEST_NAME%" %MAP_INDEX%
if errorlevel 1 exit /b 1

set "SOURCE_FILE=%SOURCE_ROOT%%SOURCE_REL%"
set "DEST_FILE=%DESTINATION_FOLDER%\%DEST_NAME%"

rem Prevent accidental directory copies; this script expects file-to-file mapping only.
if exist "%SOURCE_FILE%\*" (
    echo Mapping error at FILE%MAP_INDEX%: source is a directory, not a file.
    echo   %SOURCE_FILE%
    exit /b 1
)

if not exist "%SOURCE_FILE%" (
    echo Mapping error at FILE%MAP_INDEX%: source file not found.
    echo   %SOURCE_FILE%
    exit /b 1
)

copy /Y "%SOURCE_FILE%" "%DEST_FILE%" >nul
if errorlevel 1 (
    echo Failed to copy FILE%MAP_INDEX%: %SOURCE_REL%
    exit /b 1
)

echo Copied %SOURCE_REL% ^> %DEST_NAME%
exit /b 0

:validate_extension
rem ================================================================
rem 6) SUBROUTINE: DESTINATION EXTENSION CHECK
rem ================================================================

set "CHECK_NAME=%~1"
set "CHECK_INDEX=%~2"
set "CHECK_EXT="
set "EXT_OK="

for %%F in ("%CHECK_NAME%") do set "CHECK_EXT=%%~xF"

if "%CHECK_EXT%"=="" (
    echo Mapping error at FILE%CHECK_INDEX%: destination name has no extension.
    echo   %CHECK_NAME%
    exit /b 1
)

for %%E in (%ALLOWED_EXTENSIONS%) do (
    if /I "%%~E"=="%CHECK_EXT%" set "EXT_OK=1"
)

if not defined EXT_OK (
    echo Mapping error at FILE%CHECK_INDEX%: unsupported destination extension "%CHECK_EXT%".
    echo Allowed extensions: %ALLOWED_EXTENSIONS%
    echo Destination name: %CHECK_NAME%
    exit /b 1
)

exit /b 0