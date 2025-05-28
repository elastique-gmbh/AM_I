set arg1=%1
set PIPE=^|

setlocal EnableDelayedExpansion

echo|set /p="enc	1" > ..\touchdesigner\video_output\encoder_running.txt
ffmpeg -y -t 90 -v verbose -i ..\touchdesigner\video_output\%arg1%.mov -acodec aac -vcodec libx264 -crf 27 -preset veryfast ..\touchdesigner\video_output\upload\%arg1%.mp4
echo|set /p="enc	0" > ..\touchdesigner\video_output\encoder_running.txt