# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import time
import pyinotify

tokenizer = AutoTokenizer.from_pretrained("lmsys/vicuna-7b-v1.3")
model = AutoModelForCausalLM.from_pretrained("lmsys/vicuna-7b-v1.3", device_map = 'cuda:0')

print("Model loaded")

#Path to the necessary files
prompt_file_path = '/home/pragya/LLMCode/prompt.txt'

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
		#outputs = model.generate(inputs, pad_token_id = tokenizer.pad_token_id, bos_token_id = tokenizer.bos_token_id, eos_token_id = tokenizer.eos_token_id,max_length = 2048, temperature=0.2, do_sample=True, top_k=15, top_p=0.95)
		outputs = model.generate(inputs, pad_token_id = tokenizer.pad_token_id, bos_token_id = tokenizer.bos_token_id, eos_token_id = tokenizer.eos_token_id,max_length = 2048, temperature=0.2, do_sample=False)
		#outputs = model.generate(inputs, pad_token_id = tokenizer.pad_token_id, bos_token_id = tokenizer.bos_token_id, eos_token_id = tokenizer.eos_token_id,max_new_tokens = 10000, temperature=0.2, do_sample=False)
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
		  
	for code_piece in code:
		print(code_piece)
		
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
