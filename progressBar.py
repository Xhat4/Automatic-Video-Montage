import threading
import time
import sys
import os
from tqdm import tqdm
from proglog import ProgressBarLogger


# Definition of the progress bar
progress = tqdm(total=100, desc="Making video", unit="%", mininterval=0.1, dynamic_ncols=True)

stop_thread = False

# function to update the progress bar estimated time of execution and total time of execution
def keep_alive():
    while not stop_thread:
        time.sleep(0.5)
        progress.update(0.01)
        progress.refresh()
        time.sleep(0.5)
        progress.update(-0.01)
        progress.refresh()

# function that controls ctl+c to interrump the execution
def signal_handler(sig, frame):
    global stop_thread
    stop_thread = True
    # thread.join()
    progress.close()
    print("\nInterrupción detectada. Saliendo...")
    sys.exit(0)

# Function to update gradually the percentage
def update_progresbar(bar, target, delay=0.05):
    increment = int(target - bar.n)
    if increment > 0:
        for _ in range(increment):
            bar.update(1)
            time.sleep(delay)
                  

class SimpleLogger(ProgressBarLogger):

    def __init__(self, update_progressbar):
        super().__init__()
        self.update_progressbar = update_progressbar
        self.lastSection = 0
    
    # function to control the progres bar during the last videofile write
    def bars_callback(self, bar, attr, value,old_value=None):

        totalFrames = self.bars[bar]['total']

        if totalFrames and attr == "index": # Avoid divisions to 0 and Avoid the first call with total frames in the value field
            # Divide the total frames to 20 fragments 1 fragment for each 1% of the progressbar
            sectionSize = totalFrames / 20
            # Calculate the current section
            currentSection = int(value // sectionSize)

            # Update the progress bar when we advane one section
            if currentSection > self.lastSection and currentSection <= 20:
                self.update_progressbar(progress, (80+currentSection))
                self.lastSection = currentSection
                # self.lastSection += 1

            # print(f"value: {value} / total: {self.bars[bar]['total']}")

#function that calculate steps for progressbar when transitions are made

def monitor_temp_clips(stop_flag, files):
      totalTempClips = (len(files)*3)-2
      lastSection = 0

      while not stop_flag.is_set():
            if os.path.exists("./temp_clips"):
                  tempClips = [f for f in os.listdir("./temp_clips") if os.path.isfile(os.path.join("./temp_clips", f))]

                  sectionSize = totalTempClips / 40

                  currentSection = len(tempClips) // sectionSize

                  if currentSection > lastSection and currentSection <= 40:
                        update_progresbar(progress, (20+currentSection))
                        lastSection = currentSection

            time.sleep(1)