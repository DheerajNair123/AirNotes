##With deletion
import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from threading import Thread
import time

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Global variable for note count
note_count = 0
notes = []
note_selected = None
hover_start_time = {}
last_x, last_y = None, None  # Track previous position for smoothing


# Create a note
def create_note():
    global note_count
    note_count += 1
    note = tk.Toplevel()
    note.title(f"Note {note_count}")
    note.geometry("200x150")
    note.attributes("-topmost", True)
    text = tk.Text(note)
    text.pack(expand=True, fill='both')
    notes.append(note)


# Detect gestures
def detect_gesture():
    global note_selected, hover_start_time, last_x, last_y
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = pyautogui.size()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                x_index, y_index = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * screen_height)
                x_middle, y_middle = int(middle_finger_tip.x * screen_width), int(middle_finger_tip.y * screen_height)
                x_thumb, y_thumb = int(thumb_tip.x * screen_width), int(thumb_tip.y * screen_height)
                x_pinky, y_pinky = int(pinky_tip.x * screen_width), int(pinky_tip.y * screen_height)

                # Move cursor to index finger position
                pyautogui.moveTo(x_index, y_index, duration=0.05)

                # Detect pinch (index + thumb close together) to create a note
                pinch_distance_create = ((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2) ** 0.5
                if pinch_distance_create < 40:
                    create_note()
                    time.sleep(0.2)  # Prevent rapid note creation

                # Check if hovering over a note for more than 1 second
                hovered_note = None
                for note in notes:
                    note_x, note_y = note.winfo_x(), note.winfo_y()
                    if note_x < x_index < note_x + 200 and note_y < y_index < note_y + 150:
                        if note not in hover_start_time:
                            hover_start_time[note] = time.time()
                        elif time.time() - hover_start_time[note] > 1:
                            hovered_note = note
                            break
                    else:
                        if note in hover_start_time:
                            del hover_start_time[note]

                if hovered_note:
                    note_selected = hovered_note

                # Detect pinch (index + middle close together) to move a hovered note
                pinch_distance_move = ((x_index - x_middle) ** 2 + (y_index - y_middle) ** 2) ** 0.5
                if pinch_distance_move < 40 and note_selected:
                    if last_x is None or last_y is None:
                        last_x, last_y = x_index, y_index
                    else:
                        x_index = int(0.8 * last_x + 0.2 * x_index)
                        y_index = int(0.8 * last_y + 0.2 * y_index)
                        last_x, last_y = x_index, y_index
                    note_selected.geometry(f"200x150+{x_index}+{y_index}")
                else:
                    last_x, last_y = None, None

                # Detect pinch (thumb + pinky close together) to delete a hovered note
                pinch_distance_delete = ((x_thumb - x_pinky) ** 2 + (y_thumb - y_pinky) ** 2) ** 0.5
                if pinch_distance_delete < 40 and note_selected:
                    notes.remove(note_selected)
                    note_selected.destroy()
                    note_selected = None
                    if note_selected in hover_start_time:
                        del hover_start_time[note_selected]
                    time.sleep(0.2)  # Prevent accidental multiple deletions

        cv2.imshow("Note creation and deletion", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Run gesture detection in a separate thread
thread = Thread(target=detect_gesture)
thread.daemon = True
thread.start()

# Initialize the main Tkinter root (hidden)
root = tk.Tk()
root.withdraw()
tk.mainloop()
