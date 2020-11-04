# -*- coding: Utf-8 -*-
# http://blog.acipo.com/wave-generation-in-python/

import wave
import subprocess

obj = wave.open('../Sounds/A4.wav','r')
print("Number of channels",obj.getnchannels())
print ("Sample width",obj.getsampwidth())
print ("Frame rate.",obj.getframerate())
print ("Number of frames",obj.getnframes())
print ("parameters:",obj.getparams())
obj.close()
subprocess.call(["aplay", '../Sounds/A4.wav'])