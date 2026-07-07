import time
#from time import sleep
from pop import Pilot
#from pop.Pilot import AutoCar

car = Pilot.AutoCar()   # 객체 생성

#cds
import time
from pop import Cds
import subprocess as sp, time
from IPython.display import display, Javascript
from ipywidgets import widgets
from pop import Util
lab = []
cds=Cds(7)
lab.append(widgets.Label(value="Cds : 0"))
display(lab[-1])

dtime = time.time()
while time.time()-dtime<30:
    lab[-1].value="Cds : "+str(cds.read())
    time.sleep(0.1)

#축센서
value = car.getGyro()
print(value)

time.sleep(1)

value = car.getGyro('z')
print(value)
value = car.getGyro('y')
print(value)
value = car.getGyro('x')
print(value)

# 논블로킹 모드 재생
import pyaudio
import wave
import time

def callback(in_data,frame_count,time_info,status):
    data = w.readframes(frame_count)
    return(data,pyaudio.paContinue)

w = wave.open("/usr/share/sounds/alsa/Side_Left.wav","rb")
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(w.getsampwidth()),
                channels=w.getnchannels(),
                rate=w.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    print("main work...")
    time.sleep(0.1)

stream.stop_stream()
stream.close()
p.terminate()

#모터
dtime = time.time()
lasttime=0
sw=True
while time.time()-dtime<10:
    if time.time()-lasttime>5:
        if sw:
            AC.forward(99)
            sw=False
        else:
            AC.backward(99)
            sw=True
        lasttime=time.time()
        
AC.stop()