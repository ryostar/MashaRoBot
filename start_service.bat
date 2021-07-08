@echo off
:: Thao tác này chạy tệp loạt với tư cách là quản trị viên - UAC bắt buộc phải tắt 3
:: Đây chỉ là một cuộc đột nhập tinh vi để hoàn thành công việc vì chúng tôi lưu trữ nó trên windows.
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------
:: lệnh của bạn bắt đầu từ thời điểm này.
:: stops the service and then starts it 
net stop MashaRoBot
net start MashaRoBot
