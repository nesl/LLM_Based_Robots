import multiprocessing, threading
import os, glob
import subprocess

from config import PRIVATE_KEY

'''

Current Program Setup:
Two processes: 
1) Subtask Generator
2) Code Generator

'''

# -------------- Subtask Generator Functions --------------

def Subtask_Generator():
    return

# -------------- Code Generator Functions --------------

def Code_Generator():
    return

# -------------- Main Parent Process --------------
def main_process():

    # Create process for each process
    Subtask_Generator_Process = multiprocessing.Process(target=Subtask_Generator)
    Code_Generator_Process = multiprocessing.Process(target=Code_Generator)

    # Start the process
    Subtask_Generator_Process.start()
    Code_Generator_Process.start()

    # Wait for both process to finish
    Subtask_Generator_Process.join()
    Code_Generator_Process.join()

if __name__ == "__main__":
    main_process()