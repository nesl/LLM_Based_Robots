import subprocess
import whisper
import paramiko

hostname = '192.168.50.233'
username = 'pragya'
password = 'neslrocks!'

local_path = '/home/nesl/output.txt'
remote_path = '/home/pragya/LLMCode/instruction.txt'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

model = whisper.load_model("base")
result = model.transcribe("/home/nesl/output.wav")
print(result["text"])

with open('output.txt', 'w') as file:
    file.write(result["text"])
    file.write('\n')

try:
    ssh.connect(hostname, username=username, password=password)

    scp = ssh.open_sftp()

    scp.put(local_path, remote_path)

    print("File transferred successfuly")

finally:
    ssh.close()

