cd bin/negdata
dir /b/s/p/w *.png > neg.txt
for /f "tokens=* delims=" %%i in ('dir /b /a-d /s "*.txt"') do (move "%%i" "%%~dpi./../")