import multiprocessing, threading
import os
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
    
def file_Monitoring_And_Handling():
    # Check if the file exists
    file_index = 0
    while (True):
        file_path = f'{file_folder}/subtask_{file_index}'
        if os.path.exists(file_path):
            completed_process = subprocess.run(["python3", file_path])
            if completed_process.returncode == 0:
                file_index += 1
            else:
                exit()

def file_Execution():
    return

def File_Processing():
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


# -------------- Main Parent Process --------------
def main_process():
    # Define the file path for subtasks
    file_folder = "~/Main_System_Code/JetsonCode/subtasks"
    
    # Create threads for each process
    thread1 = multiprocessing.Process(target=User_Environment_Input)
    thread2 = multiprocessing.Process(target=File_Processing)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main_process()