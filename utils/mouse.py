import pyautogui

SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900

def map_hand_to_mouse(hand_landmarks):

    # Get the coordinates of the 9th landmark
    landmark_9th = hand_landmarks.landmark[9]
    landmark_x, landmark_y = int(landmark_9th.x * SCREEN_WIDTH), int(landmark_9th.y * SCREEN_HEIGHT)
    # Move the mouse pointer twice the distance moved
    pyautogui.moveTo(landmark_x, landmark_y)

def click():
    pyautogui.click()


