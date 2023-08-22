#need to run as sudo -E python3 speechToText.py
#!/usr/bin/env python3
import pyaudio
import wave
import whisper
import paramiko

import os
import pyinotify
import subprocess

#dependencies for Voice Activity Detection
import usb.core
import usb.util
import time
import sys
sys.path.append('/home/nesl/usb_4_mic_array')

from tuning import Tuning

#ssh remote computer information
hostname = '192.168.50.233'
username = 'pragya'
password = 'neslrocks!'

local_path = '/home/nesl/JetsonCode/output.txt'
remote_path = '/home/pragya/DesktopCode/UserTask.txt'

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 1  # refer to input device id ------------------- run get_index.py to check for correct id number
CHUNK = 1024
RECORD_SECONDS = 3 #record in 2 second intervals 
WAVE_OUTPUT_FILENAME = "/home/nesl/JetsonCode/output.wav"

mainFolder = '/home/nesl/JetsonCode/'
codeGen_file_path = mainFolder + 'desktopTransferredCode.py'

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        file_path = os.path.join(event.path, event.name)
        if file_path == codeGen_file_path:
            cur_time = time.ctime(time.time())
            print(f"Code File received")
            central_loop()

#----------------------------------------------------MAIN------------------------------------------------------------
def central_loop():
    run_code()
    record()
    transcribe()
    ssh()

#-----------------------------------------------------HELPER FUNCTIONS------------------------------------------------
def record():
    #setup code
    p = pyaudio.PyAudio()
    
    device_channels = p.get_device_info_by_host_api_device_index(0, 1).get('maxInputChannels')
    
    
    
    #voice activity detection
    if dev:
        Mic_tuning = Tuning(dev)
        while not Mic_tuning.is_voice():
            print("Waiting for voice instruction")
            time.sleep(0.2)
        if Mic_tuning.is_voice():
            stream = p.open(rate=RESPEAKER_RATE,format=p.get_format_from_width(RESPEAKER_WIDTH),channels=RESPEAKER_CHANNELS,input=True,input_device_index=RESPEAKER_INDEX,)
            frames = []
            print("* recording user task")
        while Mic_tuning.is_voice():
            for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            
        print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()   

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe():
    #run whisper base model to transcribe audio file
    model = whisper.load_model("base")
    result = model.transcribe("/home/nesl/JetsonCode/output.wav")
    print("Task:", result["text"])
    
    
    #write result to text file
    with open('/home/nesl/JetsonCode/output.txt','w') as file:
        file.write(result["text"])
        file.write('\n')

def ssh():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #establish SSH connection
    try:
        ssh.connect(hostname, username=username, password=password)
        scp = ssh.open_sftp()
        scp.put(local_path, remote_path)
        print("File transferred successfully")
    #close ssh connection
    finally:
        ssh.close()
	    
def run_code():
	try:
		result = subprocess.run(["python3", "/home/nesl/JetsonCode/desktopTransferredCode.py"], env=os.environ, check=True)
		print("Script executed successfully")
	except subprocess.CalledProcessError as e:
		print("Error executing the script", e)
	
dir_to_watch = os.path.abspath(mainFolder)
watcher_manager = pyinotify.WatchManager()    
watch_mask = pyinotify.IN_CLOSE_WRITE
watcher_manager.add_watch(dir_to_watch, watch_mask)

notifier = pyinotify.Notifier(watcher_manager, EventHandler())

record()
transcribe()
ssh()
try:
    print(f"Monitoring for code file")
    notifier.loop()
except KeyboardInterrupt:
    notifier.stop()
    print("Monitoring stopped")
	
	

