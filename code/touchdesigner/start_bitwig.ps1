$wshell = New-Object -com "Wscript.Shell"
#Start-Process -FilePath "C:\Program Files\Bitwig Studio\Bitwig Studio.exe" -ArgumentList "C:\Users\am_i\Desktop\20250507_Am-I-Bitwig_ADC-Version_01\Elastique_Am-I_30_ADC-Project.bwproject"
Start-Sleep -Seconds 18
$wshell.sendkeys(" ")