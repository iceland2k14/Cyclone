# -*- coding: utf-8 -*-
"""
Usage: python go.py

@author: iceland
"""

import random
import subprocess
import os, time, sys, math

# ANSI escape codes
# \033[<N>A : Move cursor up N lines
# \033[K   : Erase from cursor to end of line
# \033[G   : Move cursor to column 1 (start of line)

CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[K'

#==============================================================================

puzz = {int(line.split()[0]):line.split()[1] for line in open('unsolved.txt','r')}
puzz_bits = list(puzz.keys())
#==============================================================================
puzzle = random.sample(puzz_bits, 1)[0]
address = puzz[puzzle]

# Constants
LOWER_BOUND = 2 ** (puzzle - 1)
UPPER_BOUND = (2**puzzle) - 1
BIT_GAP = 2**26  # 26-bit gap 

def display_time(seconds):
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}"

#==============================================================================
print('\n[+] Starting Program.... Please Wait !')
print(f'[+] Search Mode: Sequential Random in each Loop. seq = {BIT_GAP:,}')
print(f'[+] Total Unsolved: {len(puzz_bits)} Puzzles in the bit range [{min(puzz_bits)}-{max(puzz_bits)}]')
print(f'[+] Target Selected : Puzzle #{puzzle}  with Address: {address}')

count = 0
start = time.time()
try:
    while True:
        # Generate the first random number within the valid range. 3 sample average for stability
        first_number = sum(random.SystemRandom().randrange(LOWER_BOUND, UPPER_BOUND - BIT_GAP) for _ in range(3)) // 3
      
        # Calculate the second number with a 26-bit gap
        second_number = first_number + BIT_GAP
      
        # Format both numbers as hexadecimal strings without leading zeros
        first_hex = f"{first_number:X}"  # No leading zeros
        second_hex = f"{second_number:X}"  # No leading zeros
      
        # Prepare the command with the generated random values
        command = [
            "./Cyclone",
            "-a", f"{address}",
            "-t", "24",
            "-r", f"{first_hex}:{second_hex}"
        ]
        
        el = display_time(time.time() - start)
        # Print the progress on the same line using '\r'
        #print(f'[I: {count+1}] [Puzz: {puzzle}] [T:{BIT_GAP*(count+1):,}] [{el}] [Range: {first_hex}:{second_hex}]', end='\r')
        sys.stdout.write(f'[I: {count+1}] [Puzz: {puzzle}] [T:{BIT_GAP*(count+1):,}] [Time(h:m:s): {el}]          \n')
        sys.stdout.write(f'[From: {first_hex}] [{math.log2(first_number):.5f} bit]         \n')
        sys.stdout.write(f'[To  : {second_hex}] [{math.log2(second_number):.5f} bit]        \n')
        # Move cursor up 3 lines to the beginning of the first line
        sys.stdout.write(f'{CURSOR_UP_ONE * 3}')
        sys.stdout.flush() # Ensure immediate update
    
        # Execute the command.
        # We will pipe stdout/stderr to capture it, but not print it immediately.
        # Instead of `DEVNULL`, we still need to capture it to check for "FOUND MATCH!".
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
        # Buffer to store all output from the subprocess
        subprocess_output_buffer = []
        found_match = False
        
        # Read output line by line from the subprocess
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline() # Also read stderr, in case "FOUND MATCH!" is there
    
            if not stdout_line and not stderr_line and process.poll() is not None:
                break # No more output and process has finished
    
            if stdout_line:
                subprocess_output_buffer.append(stdout_line)
                if "FOUND MATCH!" in stdout_line:
                    found_match = True
    
            if stderr_line:
                subprocess_output_buffer.append(stderr_line) # Capture stderr too
                if "FOUND MATCH!" in stderr_line: # Check stderr for match as well
                    found_match = True
    
        # After the subprocess has finished (or `found_match` becomes True and we decide to break early),
        # then check if "FOUND MATCH!" was found in the buffered output.
        if found_match:
            # Clear the current line with spaces before printing the full output
            print(' ' * 120, end='\r') # Use a sufficiently large number of spaces
    
            # Print all the buffered output from Cyclone.exe
            for line in subprocess_output_buffer:
                print(line, end="") # Print with default newline
    
            # Print your "FOUND MATCH!" banner
            print("================== FOUND MATCH! ==================")
            
            # Save to file (as before)
            with open("found_match.txt", "w") as file:
                # We need to find the "FOUND MATCH!" line again in the buffer
                # to capture the lines after it for saving to file.
                # This logic needs to be refined if the lines_after_match should be exactly 8.
                # Let's re-implement the original logic for saving to file.
                lines_to_save_for_file = []
                found_match_for_save = False
                lines_after_match_count = 0
                for line in subprocess_output_buffer:
                    if "FOUND MATCH!" in line and not found_match_for_save:
                        found_match_for_save = True
                        lines_to_save_for_file.append(line)
                    elif found_match_for_save and lines_after_match_count < 8:
                        lines_to_save_for_file.append(line)
                        lines_after_match_count += 1
                    elif found_match_for_save and lines_after_match_count >= 8:
                        break # Stop capturing lines for the file
    
                file.writelines(lines_to_save_for_file)
            
            break  # Exit the script after saving the lines
        
        # Wait for the process to complete (important even if we broke early from the loop)
        process.wait()
    
        # Check the return code of the process
        if process.returncode != 0:
            # If the process exited with an error and we haven't found a match
            # It's good to print the error output, even if it wasn't a "match"
            print(f"\nCyclone command failed with return code: {process.returncode}")
            print("--- Subprocess Error Output ---")
            for line in subprocess_output_buffer: # Print all captured output for debugging
                print(line, end="")
            print("-------------------------------")
    
        # Increment counter
        count += 1
    
except:
    exit('\n\n\nSIGINT or CTRL-C detected. Exiting gracefully. BYE')
    