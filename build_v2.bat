@echo off
setlocal enabledelayedexpansion
echo ================================
echo PyInstaller Build Script
echo ================================
echo.

echo [1/5] Checking for .spec file...
set SPEC_FILE=
for %%f in (*.spec) do (
    set SPEC_FILE=%%f
)

if not defined SPEC_FILE (
    echo No .spec file found. Will generate from Python file...
    echo.
    
    REM Count Python files
    set PY_COUNT=0
    for %%f in (*.py) do (
        set /a PY_COUNT+=1
        set PY_!PY_COUNT!=%%f
    )
    
    REM Handle different scenarios
    if !PY_COUNT!==0 (
        echo ERROR: No Python files found in current directory
        pause
        exit /b 1
    )
    
    if !PY_COUNT!==1 (
        set PYTHON_FILE=!PY_1!
        echo Found single Python file: !PYTHON_FILE!
    ) else (
        echo Found !PY_COUNT! Python files:
        for /l %%i in (1,1,!PY_COUNT!) do (
            echo [%%i] !PY_%%i!
        )
        echo.
        set /p CHOICE="Select number (1-!PY_COUNT!): "
        set PYTHON_FILE=!PY_!CHOICE!!
        
        if not defined PYTHON_FILE (
            echo ERROR: Invalid selection
            pause
            exit /b 1
        )
    )
    
    echo.
    echo Generating .spec file from: !PYTHON_FILE!
    
    REM Activate venv first
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Failed to activate virtual environment
        pause
        exit /b 1
    )
    
    REM Generate .spec file with --onefile
    pyi-makespec "!PYTHON_FILE!" --onefile --windowed
    
    if errorlevel 1 (
        echo ERROR: Failed to generate .spec file
        pause
        exit /b 1
    )
    
    REM Find the newly created .spec file
    for %%f in (*.spec) do (
        set SPEC_FILE=%%f
    )
    
    if not defined SPEC_FILE (
        echo ERROR: .spec file was not created
        pause
        exit /b 1
    )
    
    echo Generated: !SPEC_FILE!
    echo Note: You may want to edit this .spec file for custom configurations.
    echo.
) else (
    echo Found: %SPEC_FILE%
    echo.
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo [4/5] Building executable with PyInstaller...
pyinstaller --clean "%SPEC_FILE%"
if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

echo [5/6] Check for project in apps directory
FOR %%F IN ("!SPEC_FILE!") DO SET folder_name=%%~nF
SET "new_folder=C:\Users\Charlie.Jackson\Documents\Coding\Python\apps\!folder_name!"
IF NOT EXIST "!new_folder!\" (
    echo Creating app folder...
    mkdir "!new_folder!"
)

echo [6/6] Copy executable to app folder
copy /Y "dist\*.exe" "!new_folder!\"


echo.
echo ================================
echo BUILD SUCCESSFUL!
echo ================================
echo Built from: !SPEC_FILE!
echo Executable location: !new_folder!
echo.
echo Press any key to close this window...
pause >nul