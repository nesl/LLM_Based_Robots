import threading
import os
import subprocess


# Define two functions that represent your processes
def process1():
    # TODO: refine centralhub logic by changing whisper to new model
    
def process2(file_folder):
    # Check if the file exists
    file_index = 0
    while (True):
        file_path = f'{file_folder}/subtask_{file_index}'
        if os.path.exists(file_path):
            completed_process = subprocess.run(["python3", file_path])
            if completed_process.returncode == 0:
                file_index += 1

# Define the file path for subtasks
file_folder = "~/Main_System_Code/JetsonCode/subtasks"
# Create threads for each process
thread1 = threading.Thread(target=process1)
thread2 = threading.Thread(target=process2(file_folder))

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Both processes completed")
