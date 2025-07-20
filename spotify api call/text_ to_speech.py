import pyttsx3 # used to convert text to speech
import threading # used to run multiple task at the same time eg in this code like waiting for user command 
import keyboard # detects user key like any space q or any chenge how you like to change it
import json # used to store menory may be temporary 
import time # used for waiting between user command
import PyPDF2 # used for reading pdf

# a function to save the last page where u left it 
def save_progress (last_page):
    with open("progress.json", "w") as f: #here w means write and f is a variable which is defined to do the function read or write
        json.dump({"last_page": last_page}, f)

def load_progress():
    try:
        with open("progress.json", "r") as f: # here r means read
            data =n json.load(f)
            return data.get("last_page", 0) # starts from 0 if no progress is found
    except FileNotFoundError:
        return 0        

file = open("46laws_of_power.pdf", "rb") #rb stands for read binary used to read its data in raw form
read_pdf = PyPDF2.PdfReader(file)
pages = len(read_pdf.pages) # takes the pages of the pdf to know how long it needs to speak
print(f"The pdf has {pages} pages.") # the , pages, is used to mix or use the string + int

speak = pyttsx3.init() # initializing the text to speech engine 

last_page = load_progress()

start = input(f"Do you want to resume from page {last_page} (y/n): ")
if start.lower() == 'y':
    start_page = last_page
else:
    start_page = int(input(f"Where do you want to start reading: "))


# `s` variable 0 = Playing, 1 = Paused, 2 = Stopped
s = 0  

# Function to read the book and pause/resume based on the 's' variable
def read_book():
    global s, start_page

    for page_num in range(start_page, pages):
        if s == 2:
            break  # Stop reading
        
        # Pause if 's' is set to 1
        while s == 1:
            time.sleep(0.1)  # Wait until 's' is changed to 0 (resumed)

        page = read_pdf.pages[page_num]  
        page_text = page.extract_text()  

        save_progress(page_num)  #  save progress before reading
        speak.say(page_text)  
        speak.runAndWait()
        #threading.Thread(target= page_text, args=(page_text,)).start() # This is where the reading happens

# Function to control playback using keyboard input
def control_for_playback():
    global s
    
    while s != 2:  # Stop when 's' is set to 2
        if keyboard.is_pressed("space"):
            print("space key is pressed")  # Toggle pause/resume with spacebar
            if s == 0:
                s = 1  # Pause reading
                print("\nPaused!")
            else:
                s = 0  # Resume reading
                print("\nResumed!")
            time.sleep(0.5)  # Delay to prevent multiple detections

        if keyboard.is_pressed("q"):  # Stop the reading when 'q' is pressed
            s = 2  # Stop
            print("\nStopped and Progress Saved.")
            save_progress(start_page)
            speak.endLoop()  # End any ongoing speech
            break

# Run the reading function in a separate thread to allow non-blocking control
threading.Thread(target=read_book, daemon=True).start()

# Handle playback control
control_for_playback()
