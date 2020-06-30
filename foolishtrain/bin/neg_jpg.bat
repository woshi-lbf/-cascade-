cd bin/negdata
dir /b/s/p/w *.jpg > neg.txt
for /f "tokens=* delims=" %%i in ('dir /b /a-d /s "*.txt"') do (move "%%i" "%%~dpi./../")