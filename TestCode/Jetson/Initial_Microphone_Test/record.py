#need to run with sudo -E python3 record.py

import pyaudio
import wave
import whisper
import time

import usb.core
import usb.util

#from tuning import Tuning

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run get_index.py to get index
RESPEAKER_INDEX = 1  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "/home/nesl/microphoneAudio/output.wav"

p = pyaudio.PyAudio()

device_channels = p.get_device_info_by_host_api_device_index(0, 1).get('maxInputChannels')
print('Input device channels is ', device_channels)

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

#test whisper model
model = whisper.load_model("base")
start_time = time.time()
result = model.transcribe("/home/nesl/microphoneAudio/output.wav")
end_time = time.time()
print(result["text"])
print("Elapsed time:", str(end_time - start_time))
