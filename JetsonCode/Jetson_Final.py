
import wave
import whisper
import os
import paramiko
import pyaudio
import pyinotify
import subprocess
import time

#ssh remote computer information
hostname = '192.168.50.233'
username = 'pragya'
password = 'neslrocks!'

#path variables to the files
local_path = '/home/nesl/userTask.txt' #output of the Whisper model (the user task)
remote_path = '/home/pragya/LLMCode/instruction.txt'

#variables related to the microphone module
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 1  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "userTask.wav"

#load the Whisper Model
model = whisper.load_model("base")

#the directory that the EventHandler should monitor for changes
dir_to_watch = os.path.abspath('/home/nesl')
watcher_manager = pyinotify.WatchManager()
prompt_file_path = "/home/nesl/desktopTransferredCode.py"

#----------------------------- DEFINE THE EVENT HANDLER ---------------
class EventHandler(pyinotify.ProcessEvent):
    '''
    def process_IN_MODIFY(self, event):
        file_path = os.path.join(event.path, event.name)
        if file_path == prompt_file_path:
            print(f"File: {prompt_file_path} is being modified...")
    '''
    def process_IN_CLOSE_WRITE(self, event):
        file_path = os.path.join(event.path, event.name)
        if file_path == prompt_file_path:
            # Process the file update event
            cur_time = time.ctime(time.time())
            print(f"File updated: {file_path} at {cur_time}")
            central_loop()

#----------------------------- AUXILIARY FUNCTIONS ------------------

def recordAudio():
    '''
    Uses the microphone module to record the user input and store it in string form into a variable.
    '''
    
    p = pyaudio.PyAudio() #PyAudio used for filtering

    device_channels = p.get_device_info_by_host_api_device_index(0, 1).get('maxInputChannels')

    stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                input=True,
                input_device_index=RESPEAKER_INDEX,)

    print("* recording")

    frames = []

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


    #run whisper base model to transcribe audio file
    result = model.transcribe("/home/nesl/userTask.wav")
    print(result["text"])
    return result["text"]


def sendToDesktop(prompt):
    '''
    First writes the user prompt into a text file. Then sends the user prompt to the Desktop hosting the LLM.
    '''
    #write result to text file
    with open('userTask.txt','w') as file:
        file.write(prompt)
        file.write('\n')
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #establish SSH connection
    try:
        ssh.connect(hostname, username=username, password=password)
        scp = sshopen_sftp()
        scp.put(local_path, remote_path)
        print("File transferred successfully")

    #close ssh connection
    finally:
        ssh.close()

#----------------------------- MAIN LOOPED FUNCTION ------------------
def central_loop():
    '''
    Records the user given prompt, stores it in a text file, and finally send it to the Desktop machine hosting the LLM.
    '''
    #execute code
    subprocess.run(['python3', 'desktopTransferredCode.py'])
    #wait for user activation
    #prompt = recordAudio() - UNCOMMENT IN FINAL VERSION
    prompt = "Given the functions below, write Python code to make the robot move 2 meters froward." # DELETE IN FINAL VERSION
    sendToDesktop(prompt)
    

#----------------------------- MAIN CODE ------------------
watch_mask = pyinotify.IN_CLOSE_WRITE
watcher_manager.add_watch(dir_to_watch, watch_mask)

# Create the notifier and associate it with the watcher and event handler
notifier = pyinotify.Notifier(watcher_manager, EventHandler())

# run once
#prompt = recordAudio() - UNCOMMENT IN FINAL VERSION
prompt = "Given the functions below, write Python code to make the robot move 2 meters froward." # DELETE IN FINAL VERSION
sendToDesktop(prompt)

# Start monitoring for file changes
try:
    print(f"Monitoring file: {prompt_file_path}")
    notifier.loop()
except KeyboardInterrupt:
    # Exit gracefully when interrupted by Ctrl+C
    notifier.stop()
    print("Monitoring stopped")
