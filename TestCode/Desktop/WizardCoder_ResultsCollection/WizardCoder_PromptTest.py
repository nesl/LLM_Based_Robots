# Libraries
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import pyinotify
import paramiko
import torch

#-----------------------------------LOAD TOKENIZER AND MODEL----------------------------------------
tokenizer = AutoTokenizer.from_pretrained("WizardLM/WizardCoder-15B-V1.0")
#model = AutoModelForCausalLM.from_pretrained("WizardLM/WizardCoder-15B-V1.0").to("cuda")
#model = AutoModelForCausalLM.from_pretrained("WizardLM/WizardCoder-15B-V1.0", device_map='auto')
model = AutoModelForCausalLM.from_pretrained("WizardLM/WizardCoder-15B-V1.0", torch_dtype=torch.float16, device_map='sequential', max_memory={0: '49 GiB'}, revision='main', low_cpu_mem_usage = True, offload_folder='offload')
print("Model Loaded")

#Path to the necessary files
prompt_file_path = '/home/pragya/LLMCode/WizardCoderPrompt.txt'
documentation_file_path = '/home/pragya/LLMCode/WizardCoderDocumentation.txt'

#the directory that the EventHandler should monitor for changes
dir_to_watch = os.path.abspath('/home/pragya/LLMCode')
watcher_manager = pyinotify.WatchManager()

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
            central_loop(file_path)
            
#----------------------------- AUXILIARY FUNCTIONS ------------------

def generate_code(prompt_file_path):
    '''
    First, it creates the prompt by reading from the prompt file.
    Then it passes it into the LLM to generate an output. Upon receiving the output, it writes the output and the amount of time taken to produce the output to a documentation file.
    '''
    
    print("Running model.")
    # read from prompt file
    try:
        with open (prompt_file_path, 'r', , encoding='UTF-8') as prompt_file:
            prompt = prompt_file.read()
            
    except Exception as e:
        print("Error when read from file prompt.txt:", str(e))
        exit(e)
    start_time = time.time()
    # tokenize prompt and model generate
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda").input_ids
        #outputs = model.generate(inputs, pad_token_id = tokenizer.pad_token_id, bos_token_id = tokenizer.bos_token_id, eos_token_id = tokenizer.eos_token_id,max_new_tokens = 10000, temperature=0.2, do_sample=True, top_k=15, top_p=0.95)
        outputs = model.generate(inputs, pad_token_id = tokenizer.pad_token_id, bos_token_id = tokenizer.bos_token_id, eos_token_id = tokenizer.eos_token_id,max_new_tokens = 10000, temperature=0.2, do_sample=False)
    except Exception as e:
        print("Error when tokenize input the generate output:", str(e))
        exit(e)

    # decode output
    try:
        code = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    except Exception as e:
        print("Error when decoding:", str(e))
        exit(e)
	
    end_time = time.time()
    # save to code file
    try:
        with open(documentation_file_path, 'a', encoding='UTF-8') as documentation_file:
            documentation_file.write('------------------------------------------new prompt and output------------------------------------------\n')
            for item in code:
                print(item)
                documentation_file.write(item)
            documentation_file.write("Time used (unit: s): ")
            documentation_file.write(str(end_time - start_time))
            documentation_file.write("\n\n\n\n")
            print("Finish recording results")
    except Exception as e:
        print("Error when write file LLM_genereated_code_test.py:", str(e))
        exit(e)
    time_used = end_time - start_time
    print("Finish Generating Code:", time_used)

#----------------------------- MAIN LOOPED FUNCTION ------------------
def central_loop(prompt_file_path):
    '''
    Runs the LLM with the prompt given and writes the Python code portion of the output to a documentation file using the generate_code function.
    '''
    generate_code(prompt_file_path)


#----------------------------- ACTIVATING LOOP ------------------
# Add the directory to the watcher
# watch_mask = pyinotify.IN_MODIFY | pyinotify.IN_CLOSE_WRITE
watch_mask = pyinotify.IN_CLOSE_WRITE
watcher_manager.add_watch(dir_to_watch, watch_mask)

# Create the notifier and associate it with the watcher and event handler
notifier = pyinotify.Notifier(watcher_manager, EventHandler())

# Start monitoring for file changes
try:
    print(f"Monitoring file: {prompt_file_path}")
    notifier.loop()
except KeyboardInterrupt:
    # Exit gracefully when interrupted by Ctrl+C
    notifier.stop()
    print("Monitoring stopped")
    


    
    

