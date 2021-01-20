@echo off
set "var=%~dp0"
cd %var%

:: Create temp file of echo %PATH% results
if not exist "%var%/temp" mkdir temp
echo %PATH%> temp/fn_temp.txt

:: Run setup.py
setup.py > temp/setup_return.txt
set /p OUT=<temp/setup_return.txt
IF "%OUT%" == "0" (
    echo FastNav already added to PATH... Skipping
    init.py
    pause
    )
IF "%OUT%" == "1" (
    echo Adding FastNav to PATH... (This may take awhile^)
    setx /m PATH "%var%bat;%PATH%" && (
        echo FastNav is now usable in the command line
        echo:
        echo Do 'fn -h' for help 'fn -docs' for documentation
        echo:
        init.py
        pause
    ) || (
        echo Please run setup.bat as administrator
        pause
    )
        )