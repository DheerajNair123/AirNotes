# AirNotes

## Overview
**AirNotes** is a gesture-controlled sticky notes application that allows users to create, move, and delete notes using hand gestures. It uses **Python, OpenCV, MediaPipe, Tkinter, and PyAutoGUI** to track hand movements and interact with on-screen notes seamlessly.

## Features
- ✍️ **Create Notes:** Pinch **(Index + Thumb)** to create a new note.
- 🖱️ **Move Notes:** Hover over a note for **1 second**, then pinch **(Index + Middle)** to move it.
- 🗑️ **Delete Notes:** Pinch **(Thumb + Pinky)** while hovering over a note to delete it.
- 🎯 **Cursor Control:** The cursor follows the index finger movement.
- 🏗️ **Multiple Notes:** Supports creating and managing multiple notes at once.

## Requirements
Ensure you have the following installed:
- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI
- Tkinter (comes pre-installed with Python)

You can install the required dependencies using:
```bash
pip install opencv-python mediapipe pyautogui
```

## Installation & Usage
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/AirNotes.git
   cd AirNotes
   ```
2. **Run the Application**
   ```bash
   python main.py
   ```
3. **Use Hand Gestures to Interact with Notes!**

## How It Works
1. **Hand Tracking:** Uses **MediaPipe** to detect hand landmarks.
2. **Gesture Recognition:** Detects specific pinching gestures to trigger actions.
3. **Tkinter Notes:** Creates sticky notes that can be typed on, moved, or deleted.
4. **PyAutoGUI Integration:** Moves the cursor based on finger movements.

## Controls
| Gesture | Action |
|---------|--------|
| ✋ Cursor follows index finger | Move cursor |
| 🤏 Index + Thumb pinch | Create a new note |
| 🖖 Hover 1 sec + Index + Middle pinch | Move the hovered note |
| ✂️ Thumb + Pinky pinch | Delete the hovered note |

## Future Enhancements 🚀
- ✨ Resize notes using gestures
- 🎨 Change note colors
- 🔊 Voice-to-text integration

## License
MIT License - Feel free to modify and improve! 😊

---

🎯 **Built with Passion & Gestures!** ✋🤏

