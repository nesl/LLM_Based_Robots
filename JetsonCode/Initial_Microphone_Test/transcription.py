import sys
sys.path.append('/home/nesl/.local/lib/python3.9/site-packages')
import whisper
#module_location = whisper.__file__
#print(module_location)
model = whisper.load_model("base")
result = model.transcribe("/home/nesl/output.wav")

#result is of type string
print(type(result["text"]))

file_path = '/home/nesl/file.txt'

with open(file_path, 'w') as file:
    file.write(result["text"])

# for key in result.keys():
#     print(key)
    
# for key, value in result.items():
#     print(key, value)

print(result["text"])