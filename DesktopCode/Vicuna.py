# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import time
import pyinotify
import torch

tokenizer = AutoTokenizer.from_pretrained("lmsys/vicuna-7b-v1.3")
model = AutoModelForCausalLM.from_pretrained("lmsys/vicuna-7b-v1.3", device_map = 'cuda:0')
#model = AutoModelForCausalLM.from_pretrained("lmsys/vicuna-7b-v1.3", torch_dtype=torch.float16, device_map='sequential', max_memory={1: '12 GiB'}, revision='main', low_cpu_mem_usage = True, offload_folder='offload')
print("Model loaded")

#Path to the necessary files
prompt_file_path = '/home/pragya/LLMCode/VicunaPrompt.txt'
code_file_path = '/home/pragya/LLMCode/VicunaDocumentation.txt'

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
            generate_code(file_path)
            

def generate_code(prompt_file_path):
	print("Running model.")
	# read from prompt file
	try:
		with open (prompt_file_path, 'r') as prompt_file:
			prompt = prompt_file.read()
	except Exception as e:
		print("Error when read from file prompt.txt:", str(e))
		exit(e)

	start_time = time.time()
	# tokenize prompt and model generate
	try:
		inputs = tokenizer(prompt, return_tensors="pt").to("cuda").input_ids
		outputs = model.generate(inputs ,max_length = 2048, temperature=0.2, top_p=1)
		#outputs = model.generate(inputs,max_length = 2048, temperature=0.2, do_sample=False)
	except Exception as e:
		print("Error when tokenize input the generate output:", str(e))
		exit(e)

	end_time = time.time()
	# decode output
	try:
		code = tokenizer.batch_decode(outputs, skip_special_tokens=True)
	except Exception as e:
	  	print("Error when decoding:", str(e))
	  	exit(e)
		  
	# save to code file
	try:
		with open(code_file_path, 'a', encoding='UTF-8') as code_file:
			code_file.write('------------------------------------------new prompt and output------------------------------------------\n')
			for item in code:
				print(item)
				code_file.write(item)
			code_file.write("Time used (unit: s): ")
			code_file.write(str(end_time - start_time))
			code_file.write("\n\n\n\n")
			print("Finish recording results")
	except Exception as e:
		print("Error when write file LLM_genereated_code_test.py:", str(e))
		exit(e)
		
	time_used = end_time - start_time
	print("Finish Generating Code:", time_used)
		
#the directory that the EventHandler should monitor for changes
dir_to_watch = os.path.abspath('/home/pragya/LLMCode')
watcher_manager = pyinotify.WatchManager()

# Add the directory to the watcher
# watch_mask = pyinotify.IN_MODIFY | pyinotify.IN_CLOSE_WRITE
watch_mask = pyinotify.IN_CLOSE_WRITE
watcher_manager.add_watch(dir_to_watch, watch_mask)

# Create the notifier and associate it with the watcher and event handler
notifier = pyinotify.Notifier(watcher_manager, EventHandler())

# run once
generate_code(prompt_file_path)

# Start monitoring for file changes
try:
    print(f"Monitoring file: {prompt_file_path}")
    notifier.loop()
except KeyboardInterrupt:
    # Exit gracefully when interrupted by Ctrl+C
    notifier.stop()
    print("Monitoring stopped")
