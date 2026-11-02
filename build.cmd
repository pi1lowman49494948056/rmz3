@echo off
rem ---------------------------------------------------------------------------
rem rmz3 build launcher.  Double-click to build, or run "build.cmd -nopause"
rem from a terminal.  Produces E:\rmz3\rmz3\rmz3.gba.
rem ---------------------------------------------------------------------------
chcp 65001 >nul
setlocal

set "BASH=E:\rmz3\Mysys\usr\bin\bash.exe"
set "BUILD_SH=C:\Users\65437\Documents\deepseek-harness\default-workspace\build.sh"

if not exist "%BASH%" (
    echo [ERROR] bash not found: %BASH%
    goto :done
)
if not exist "%BUILD_SH%" (
    echo [ERROR] build.sh not found: %BUILD_SH%
    goto :done
)

echo Building rmz3 ...
"%BASH%" --noprofile --norc "%BUILD_SH%"
if errorlevel 1 (
    echo.
    echo [FAILED] build error - see build.log
) else (
    echo.
    echo [OK] E:\rmz3\rmz3\rmz3.gba
)

:done
if /i not "%~1"=="-nopause" pause
endlocal
