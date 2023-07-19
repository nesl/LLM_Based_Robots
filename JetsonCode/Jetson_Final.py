import pyaudio
import wave
import whisper
import paramiko

#ssh remote computer information
hostname = '192.168.50.233'
username = 'pragya'
password = 'neslrocks!'

#path variables to the files
local_path = '/home/nesl/output.txt'
remote_path = '/home/pragya/LLMCode/instruction.txt'

#variables related to the microphone module
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 1  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

#load the Whisper Model
model = whisper.load_model("base")

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
    result = model.transcribe("/home/nesl/output.wav")
    print(result["text"])
    return result["text"]


def sendToDesktop(prompt):
    '''
    First writes the user prompt into a text file. Then sends the user prompt to the Desktop hosting the LLM.
    '''
    #write result to text file
    with open('output.txt','w') as file:
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
    prompt = recordAudio()
    sendToDesktop(prompt)
    

#----------------------------- MAIN CODE ------------------
central_loop()
