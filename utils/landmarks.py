# landmarks.py
import cv2 as cv
import copy
import itertools

# This function calculates the list of landmarks for a hand in the image
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []
    # for each landmark, calculate landmark points and append to list
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])
    return landmark_point

# This function normalizes and re-centers the landmark list for use in classification
def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    # convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
    # convert to 1-dimensional list
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
    # normalize by dividing each element by the max absolute value in the list
    max_value = max(list(map(abs, temp_landmark_list)))
    def normalize_(n):
        return n / max_value
    temp_landmark_list = list(map(normalize_, temp_landmark_list))
    return temp_landmark_list

def draw_landmarks(image, hand_landmarks):
    # Define landmark connections for visualization
    connections = [[0, 1], [1, 2], [2, 3], [3, 4],       # Thumb
                   [0, 5], [5, 6], [6, 7], [7, 8],       # Index finger
                   [0, 9], [9, 10], [10, 11], [11, 12],  # Middle finger
                   [0, 13], [13, 14], [14, 15], [15, 16], # Ring finger
                   [0, 17], [17, 18], [18, 19], [19, 20]] # Pinky finger
    # Draw landmarks
    for landmark in hand_landmarks.landmark:
        x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
        cv.circle(image, (x, y), 5, (255, 255, 255), -1)

    # Draw connections
    for connection in connections:
        x0, y0 = int(hand_landmarks.landmark[connection[0]].x * image.shape[1]), int(hand_landmarks.landmark[connection[0]].y * image.shape[0])
        x1, y1 = int(hand_landmarks.landmark[connection[1]].x * image.shape[1]), int(hand_landmarks.landmark[connection[1]].y * image.shape[0])
        cv.line(image, (x0, y0), (x1, y1), (255, 255, 255), 2)
    

def draw_info_text(image, fps, handedness, hand_sign_text):

    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text
    cv.putText(image, info_text, (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
    return image
