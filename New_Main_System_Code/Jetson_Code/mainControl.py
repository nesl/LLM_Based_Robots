import multiprocessing, threading
import os, glob
import subprocess

'''
Possible program improvements:
- If more efficient, switch from multithreading to multiprocessing.

Current Program Setup:
Two processes with two processes in each: 
1) User-Interaction
    1 - recording: Records user instruction
    2 - speech_Processing: Converts audio to text 
2) File Processing
    1 - file_Monitoring_And_Handling: monitors files sent into system
    2 - file_Execution: Runs files found and fetched by file_monitoring system

'''

# -------------- User-Interaction Process Functions --------------

'''
Implementation Notes and Recommendation:
- Write the code for using the microphone in a separate module and import it.
'''

def recording():
    # TODO: Insert code that records from microhpone interface
    while True:
        return
    return

def speech_Processing():
    # TODO: Insert code that handles conversion from speech ot text
    while True:
        return
    return

def User_Environment_Input():
    '''
    - The microphone constantly listens for user commands/instructions
    - Speech to text conversion
    '''

    recording_thread = threading.thread(target=recording)
    speechProcessing_thread = threading.thread(target=speech_Processing)

    # Start the threads
    recording_thread.start()
    speechProcessing_thread.start()

    # Wait for both threads to finish (which will never occur unless program is forcefully stopped or crashes)
    recording_thread.join()
    speechProcessing_thread.join()

    return

# -------------- File-Procesisng Process Functions --------------
    
def File_Processing():
    '''
    - Executes each received python file based on chronological order of sending
    - If exit file received, immediately terminates current process
    '''

    main_path = os.path.abspath(__file__); main_path = main_path[:main_path.rfind("/")] + "/codeFiles/"  # Path in which code files are received
    file_process = subprocess.Popen([":"], shell=True) # Shell command : does nothing
    file_number = 1

    while (True):
        
        # Check to see if an exit file exists
        if("exit.py" in os.listdir(main_path)): 
            # If a subtask is currently executing, terminate the process
            if (file_process.poll() != None): file_process.terminate()
            # Create list of all files in the code folder, sorted by creation time
            files = list(filter(os.path.isfile, glob.glob(main_path+"/*.py")))
            files.sort(key=os.path.getctime)
            exit_index = files.index(main_path+"exit.py")
            # Delete all the files on the system before it (except for mainControl.py)
            for file in files[:exit_index+1]:
                os.remove(main_path+file)
            # Reset file count number to 1
            file_number = 1
        
        # If the current subtask not done executing, continue
        if(file_process.poll() == None): continue

        # Check to see if the current file number exists. If does, execute and increment file_number
        desired_subtask_file = "subtask_"+str(file_number)+".py"
        if(desired_subtask_file in os.listdir(main_path)):
            file_process = subprocess.Popen(["python3", desired_subtask_file])
            if file_number >= 255: file_number = 1
            else: file_number+=1


# -------------- Main Parent Process --------------
def main_process():

    # Create process for each process
    User_Environment_Input_Process = multiprocessing.Process(target=User_Environment_Input)
    File_Processing_Process = multiprocessing.Process(target=File_Processing)

    # Start the process
    User_Environment_Input_Process.start()
    File_Processing_Process.start()

    # Wait for both process to finish
    User_Environment_Input_Process.join()
    File_Processing_Process.join()

if __name__ == "__main__":
    main_process()

'''
Extra Notes:
Threads are smaller/cheaper than processes, since threads share the same memory whereas processes each have their own copy. So might use split into two threads when doing a task that is relatively short/requires a lot of sharing of data, whereas you might split into two processes for longer, more independent tasks
'''