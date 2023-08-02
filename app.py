#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import cv2 as cv
import mediapipe as mp
from gtts import gTTS
import os
import threading
import datetime
import pandas as pd

from model import KeyPointClassifier
from utils import CvFpsCalc

from utils.maps import get_taxi_charge
from utils.weather import get_weather
from utils.spotify import open_spotify_and_play_music
from utils.youtube import play_youtube_video_in_brave
from utils.time import say_current_time
from utils.mouse import map_hand_to_mouse, click
from utils.landmarks import calc_landmark_list, pre_process_landmark, draw_landmarks, draw_info_text

from config import GOOGLE_MAPS_API_KEY, WEATHER_API_KEY

# Main function for running the program
def main():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 540)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
            static_image_mode='store_true',
            max_num_hands=1, 
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )

    # Load the key point classifier
    keypoint_classifier = KeyPointClassifier()

    # Load the labels for the classifiers
    with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = [row[0] for row in csv.reader(f)]

    # Set up some other necessary variables
    cvFpsCalc = CvFpsCalc(buffer_len=10)
    
    # To prevent instantaneous trigger of gestures
    prev_gestures = [None] * 50
    current_gesture_count = 0

    # Main loop for capturing and processing video frames
    while True:
        # Get the current FPS
        fps = cvFpsCalc.get()

        # Handle any key presses
        key = cv.waitKey(10)
        if key == 27:  # If the ESC key is pressed, break the loop
            break

        # Capture a frame from the video
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # Mirror the image
        debug_image = copy.deepcopy(image)

        # Process the image to detect hand landmarks
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # Calculate landmarks
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # Convert to relative coordinates and normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)

                # Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                 # Log the data
                log_data(datetime.datetime.now(), pre_processed_landmark_list, hand_sign_id)
                
                prev_gestures.pop(0)  # Remove the oldest gesture
                prev_gestures.append(hand_sign_id)  # Add the new gesture

                # If the new gesture is the same as the last one, increment the count
                if prev_gestures[-1] == prev_gestures[-2]:
                    current_gesture_count += 1
                else:  # Otherwise, reset the count
                    current_gesture_count = 0

                # If the current gesture has been detected 50 times in a row, perform the action
                if current_gesture_count >= 25:
                    if hand_sign_id == 0:
                        thread = threading.Thread(target=greet_user)
                        thread.start()
                    elif hand_sign_id == 1:
                        get_weather(WEATHER_API_KEY)
                    elif hand_sign_id == 2:
                        open_spotify_and_play_music()
                    elif hand_sign_id == 3:
                        play_youtube_video_in_brave()
                    elif hand_sign_id == 4:
                        get_taxi_charge(GOOGLE_MAPS_API_KEY)
                    elif hand_sign_id == 5:
                        say_current_time()
                    current_gesture_count = 0
                if hand_sign_id == 8:
                    map_hand_to_mouse(hand_landmarks)
                if hand_sign_id == 9:
                    click()
                debug_image = draw_info_text(
                    debug_image,
                    fps,
                    handedness,
                    keypoint_classifier_labels[hand_sign_id],
                )
                draw_landmarks(debug_image,hand_landmarks)

        # Show image
        cv.putText(debug_image, "FPS:" + str(fps), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv.LINE_AA)
        cv.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()

def greet_user():
    text_to_speak = (
                    "Hi Jeason"
                    "What can I do for you?"
                    )
                    # Create a gTTS object and save it to a temporary file
    tts = gTTS(text=text_to_speak, lang="en", slow=False)
    tts.save("wake.mp3")
    os.system("afplay -r 1.5 wake.mp3")

def log_data(timestamp, landmarks, hand_sign_id):
    # Prepare a DataFrame with the data
    df = pd.DataFrame([[timestamp, landmarks, hand_sign_id]], 
                      columns=['timestamp', 'landmarks', 'hand_sign_id'])
    
    # Append the data to 'log.csv'
    df.to_csv('log.csv', mode='a', header=False, index=False)

if __name__ == '__main__':
    main()
