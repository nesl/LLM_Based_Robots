# Libraries
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import pyinotify
import paramiko
import torch
import textwrap

#-----------------------------------LOAD TOKENIZER AND MODEL----------------------------------------
tokenizer = AutoTokenizer.from_pretrained("WizardLM/WizardCoder-15B-V1.0")
model = AutoModelForCausalLM.from_pretrained("WizardLM/WizardCoder-15B-V1.0", torch_dtype=torch.float16, device_map='sequential', max_memory={0: '49 GiB'}, revision='main', low_cpu_mem_usage = True, offload_folder='offload')
print("Model Loaded")

#Path to the necessary files
mainFolder = '/home/pragya/LLMCode/FinalWizardCoder/'
userTask_file_path = mainFolder + 'UserTask.txt'
promptStructure_file_path = mainFolder + 'PromptStructure.txt'
documentation_file_path = mainFolder + 'results.txt'

#the directory that the EventHandler should monitor for changes
dir_to_watch = os.path.abspath(mainFolder)
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
        if file_path == userTask_file_path:
            # Process the file update event
            cur_time = time.ctime(time.time())
            print(f"File updated: {file_path} at {cur_time}")
            central_loop()
            
#----------------------------- AUXILIARY FUNCTIONS ------------------
def generate_code(bootup):
    '''
    First, it creates the prompt by appending inserting the user input into the general prompt file with the APIs and other descriptions.
    Then it passes it into the LLM to generate an output. Upon receiving the output, it writes only the code portion of the output into a .py file.
    '''
    
    print("Reading prompt.")
    # read from prompt file
    try:
        with open(promptStructure_file_path, 'r', encoding='UTF-8') as prompt_file:
            prompt = prompt_file.read()
            
        with open (userTask_file_path, 'r', encoding='UTF-8') as task_file:
        	userTask = task_file.read()
                	
    except Exception as e:
        print("Error when reading files:", str(e))
        exit(e)
    
    #Lowercase the first letter of the first word in the usertask
    userTask = userTask[0].lower() + userTask[1:]
    
    #Remove new line characters from userTask string
    userTask = userTask.replace("\n", "")
    #Replace holder for user task with actual user task
    prompt = prompt.replace('<USER TASK>', userTask)
    
    start_time = time.time()
    # tokenize prompt and model generate
    print("Running model.")
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
    
    if bootup == 1:
    	return
    
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
def central_loop():
    '''
    First, it runs the LLM with the prompt given and writes the Python code portion of the output to a file using the generate_code function.
    Then it sends the generated Python code file to the Jetson using the write_to_comp function.
    '''

    generate_code(0)

#----------------------------- Model BootUp ------------------

def initialModelBootUp():
    bootPrompts_path = mainFolder + 'BootUpPrompts.txt'
    
    with open(bootPrompts_path, 'r') as file:
        prompts = file.readlines()
        
    # Strip newline characters and create a list of lines
    prompt_list = [prompt.strip() for prompt in prompts]
    print(prompt_list)
    for prompt in prompt_list:
        with open(userTask_file_path, 'w') as file:
            file.write(prompt)
        generate_code(1)
    
    print("BootUp Files successfully run.")
        
initialModelBootUp()

#----------------------------- ACTIVATING LOOP ------------------
# Add the directory to the watcher
# watch_mask = pyinotify.IN_MODIFY | pyinotify.IN_CLOSE_WRITE
watch_mask = pyinotify.IN_CLOSE_WRITE
watcher_manager.add_watch(dir_to_watch, watch_mask)

# Create the notifier and associate it with the watcher and event handler
notifier = pyinotify.Notifier(watcher_manager, EventHandler())

# Start monitoring for file changes
try:
    print(f"Monitoring file: {userTask_file_path}")
    notifier.loop()
except KeyboardInterrupt:
    # Exit gracefully when interrupted by Ctrl+C
    notifier.stop()
    print("Monitoring stopped")
    


    
    

