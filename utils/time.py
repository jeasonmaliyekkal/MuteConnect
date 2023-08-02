from gtts import gTTS
import os
from datetime import datetime

def get_current_time():
    # Get the current time
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    return current_time

def say_current_time():
    # Get the current time in the format "HH:MM"
    current_time = get_current_time()

    # Generate the message and play it out loud
    message = f"The current time is {current_time}."
    speech = gTTS(text=message, lang='en')
    speech.save("time.mp3")
    os.system("afplay -r 1.5 time.mp3")