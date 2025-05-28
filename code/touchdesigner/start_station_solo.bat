timeout /T 30
start "" "C:\Program Files\Bitwig Studio\Bitwig Studio.exe" "C:\Users\am_i\Desktop\20250507_Am-I-Bitwig_ADC-Version_01\Elastique_Am-I_30_ADC-Project.bwproject"
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& 'C:\Users\am_i\Desktop\MirrorMeBot\touchdesigner\start_bitwig.ps1'"
timeout /T 20
start "" /D C:\Users\am_i\Desktop\MirrorMeBot\mirror-me-player\ C:\Users\am_i\Desktop\MirrorMeBot\mirror-me-player\.venv-bot\Scripts\pythonw.exe __main__.py
timeout /T 5
start "" "C:\Program Files\Derivative\TouchDesigner.2023.12000\bin\Touchdesigner.exe" mirror-me-vr-station_solo_experience.toe