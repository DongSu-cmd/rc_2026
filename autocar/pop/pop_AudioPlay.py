from numpy import record


from pop import AudioRecord, AudioPlay 
import time 
 
with AudioRecord("my_record.wav") as record: 
    record.run() 
    print("Start Recording...")     
 
    for _ in range(5): 
       time.sleep(1) 
 
    record.stop() 
    print("Stop Recording...")     
 
# 논블로킹 모드, 반복재생 
with AudioPlay("my_record.wav", False, True) as play:    
    play.run() 
    print("Start Play...") 
    for _ in range(12):   
        time.sleep(1) 
 
    play.stop() 
    print("Stop play...")

    01: from gtts import gTTS 
02: import subprocess 
03:  
04: try: 
05:     
while True: 
06:         
f = input("Enter of file name: ") 
07:         
t = input("Enter of Text: ") 
08:         
l = input("Select language (ko | en): ") 
09:          
10:         
tts = gTTS(t, lang=l) 
11:         
tts.save(f + ".mp3") 
12:  
13:         
with subprocess.Popen(["play", f + ".mp3"]) as p: 
14:             
p.wait() 
15: except KeyboardInterrupt: 
16:     
pass 