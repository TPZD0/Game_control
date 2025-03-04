import cv2
import mediapipe as mp
import pydirectinput
import time
import json

CONFIG_FILE = "gesture_config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"gesture_map": {}}

config = load_config()
gesture_map = config.get("gesture_map", {})

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

screen_width, screen_height = pydirectinput.size()
pydirectinput.FAILSAFE = False

cap = cv2.VideoCapture(0)
border_width = 50
held_keys = {}

def hold_key(key):
    if key not in held_keys:
        pydirectinput.keyDown(key)
        held_keys[key] = True

def release_key(key):
    if key in held_keys:
        pydirectinput.keyUp(key)
        del held_keys[key]

def get_finger_states(hand_landmarks, is_right_hand):
    finger_states = [0, 0, 0, 0, 0]
    if is_right_hand:
        finger_states[0] = 1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0
    else:
        finger_states[0] = 1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0
    
    for i, tip in enumerate([8, 12, 16, 20]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[i + 1] = 1
    
    return finger_states

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    move_mouse = False
    action_text_right = "No action (Right Hand)"
    action_text_left = "No action (Left Hand)"
    active_keys = set()

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[i]
            is_right_hand = handedness.classification[0].label == "Right"
            
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_states = get_finger_states(hand_landmarks, is_right_hand)
            
            if is_right_hand:
                index_tip = hand_landmarks.landmark[8]
                x, y = int(index_tip.x * w), int(index_tip.y * h)
                screen_x = int((x - border_width) * screen_width / (w - 2 * border_width))
                screen_y = int((y - border_width) * screen_height / (h - 2 * border_width))
                
                if finger_states == [0, 1, 1, 0, 0]:
                    move_mouse = True
                    action_text_right = "Moving Mouse"
                elif finger_states == [1, 1, 1, 0, 0]:
                    move_mouse = False
                    action_text_right = "Stop Mouse"
                elif finger_states == [1, 0, 1, 0, 0]:
                    pydirectinput.mouseDown()
                    time.sleep(0.05)
                    pydirectinput.mouseUp()
                    action_text_right = "Left Click"
                elif finger_states == [1, 1, 0, 0, 0]:
                    pydirectinput.mouseDown(button='right')
                    time.sleep(0.05)
                    pydirectinput.mouseUp(button='right')
                    action_text_right = "Right Click"
                
                if move_mouse:
                    pydirectinput.moveTo(screen_x, screen_y)
            else:
                key = next((k for k, v in gesture_map.items() if v == finger_states), None)
                if key:
                    hold_key(key)
                    active_keys.add(key)
                    action_text_left = f"Holding {key.upper()}"

        for key in list(held_keys.keys()):
            if key not in active_keys:
                release_key(key)
                action_text_left = "Released Key"
    
    cv2.putText(frame, action_text_right, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, action_text_left, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.imshow('Hand Tracking with Key Hold', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()