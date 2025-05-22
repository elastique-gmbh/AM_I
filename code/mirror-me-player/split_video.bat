set arg1=%1
set PIPE=^|

setlocal EnableDelayedExpansion

set i=1
set "fn!i!=%arg1:_=" & set /A i+=1 & set "fn!i!=%"
set fn

:: Split input video in 3 Streams
set "filter=[0:v]split=3[in1][in2][in3];"
:: Crop out user parts
set "filter=%filter%[in1]crop=in_w/3:1920:0:0[out1];"
set "filter=%filter%[in2]crop=in_w/3:1920:in_w/3:0[out2];"
set "filter=%filter%[in3]crop=in_w/3:1920:in_w/3*2:0[out3];"

:: split audio channels into seperate streams
set "filter=%filter%[0:a]channelsplit=channel_layout=5.0[FL][FR][FC][BL][BR];"
:: create stereo ambient loop
set "filter=%filter%[BL][BR]join=inputs=2:channel_layout=stereo[ambient];"
:: split audio stream into 3 streams for 3 users
set "filter=%filter%[ambient]asplit=3[ambient1][ambient2][ambient3];"

:: create stereo streams from mono user channels
set "filter=%filter%[FL]asplit[FL1][FL2];"
set "filter=%filter%[FR]asplit[FR1][FR2];"
set "filter=%filter%[FC]asplit[FC1][FC2];"
set "filter=%filter%[FL1][FL2]amerge=inputs=2[BOT1];"
set "filter=%filter%[FR1][FR2]amerge=inputs=2[BOT2];"
set "filter=%filter%[FC1][FC2]amerge=inputs=2[BOT3];"

:: merge ambient and user channels
set "filter=%filter%[ambient1][BOT1]amerge=inputs=2,pan=stereo%PIPE%c0<c0+c2%PIPE%c1<c1+c3[audio1];"
set "filter=%filter%[ambient2][BOT2]amerge=inputs=2,pan=stereo%PIPE%c0<c0+c2%PIPE%c1<c1+c3[audio2];"
set "filter=%filter%[ambient3][BOT3]amerge=inputs=2,pan=stereo%PIPE%c0<c0+c2%PIPE%c1<c1+c3[audio3];"
echo|set /p="enc	1" > ..\touchdesigner\video_output\encoder_running.txt
ffmpeg -y -t 90 -v verbose -i ..\touchdesigner\video_output\%arg1%.mov -filter_complex "%filter%" -map "[out1]" -map "[audio1]" -acodec aac -vcodec libx264 -crf 27 -preset veryfast ..\touchdesigner\video_output\upload\%fn1%.mp4 -map "[out2]"  -map "[audio2]" -acodec aac -vcodec libx264 -crf 27 -preset veryfast ..\touchdesigner\video_output\upload\%fn2%.mp4 -map "[out3]" -map "[audio3]" -acodec aac -vcodec libx264 -crf 27 -preset veryfast ..\touchdesigner\video_output\upload\%fn3%.mp4
echo|set /p="enc	0" > ..\touchdesigner\video_output\encoder_running.txt