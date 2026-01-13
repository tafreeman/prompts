@echo off
setlocal

REM Double-clickable runner for the Tools Ecosystem Evaluator.
REM For options, run from a terminal:
REM   Run-Tools-Ecosystem-Eval.cmd -Parallel -CaptureConsoleOutput

set SCRIPT=%~dp0scripts\run-tools-ecosystem-eval.ps1

powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" %*
set EXITCODE=%ERRORLEVEL%

echo.
echo Exit code: %EXITCODE%
echo.
pause
exit /b %EXITCODE%
