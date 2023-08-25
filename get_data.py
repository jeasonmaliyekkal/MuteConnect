import csv
import cv2 as cv
import mediapipe as mp
import copy
import itertools
from utils.landmarks import calc_landmark_list, pre_process_landmark

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

def logging_csv(number, landmark_list):
    # log key point
    csv_path = 'model/classifier/data.csv'
    with open(csv_path, 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([number, *landmark_list])
    return

number_of_classes = 10
dataset_size = 1000

for j in range(5,number_of_classes):

    print('Collecting data for class {}'.format(j))

    done = False
    while True:
        # Capture a frame from the video
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # Mirror the image
        cv.putText(image, 'Ready? Press "Q" ! :)', (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv.LINE_AA)
        cv.imshow('frame', image)
        if cv.waitKey(25) == ord('q'):
            break

    counter = 0
    while counter < dataset_size:
        # Handle any key presses
        key = cv.waitKey(10)
        if key == 27:  # If the ESC key is pressed, break the loop
            break

        # Capture a frame from the video
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # Mirror the image
        
        # Process the image to detect hand landmarks
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                    results.multi_handedness):
                # Calculate landmarks
                landmark_list = calc_landmark_list(image, hand_landmarks)

                # Convert to relative coordinates and normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)
                # Save training data
                logging_csv(j, pre_processed_landmark_list)
        counter =  counter + 1
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        cv.putText(image, 'Collecting data for class {}'.format(j), (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv.LINE_AA)
        cv.imshow('frame', image)

cap.release()
cv.destroyAllWindows()