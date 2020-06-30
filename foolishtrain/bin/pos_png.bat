cd bin/posdata
dir /b/s/p/w *.png > pos.txt
for /f "tokens=* delims=" %%i in ('dir /b /a-d /s "*.txt"') do (move "%%i" "%%~dpi./../")