#!/usr/bin/env python3
import os
# .................................................... Ask Frame Name
FrameName=input('       Type frame name: ')
VideoName=input('Type output video name: ')
# ..................................................... FFmpeg command
command='ffmpeg -r 30 -f image2 -i '+FrameName
command+='%08d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p '
command+=VideoName
os.system(command)




